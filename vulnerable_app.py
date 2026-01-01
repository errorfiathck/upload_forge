from flask import Flask, request, send_from_directory, render_template_string
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Vulnerable Upload</title>
    <style>
        body { font-family: sans-serif; background: #222; color: #fff; padding: 50px; text-align: center; }
        .box { background: #333; padding: 20px; border-radius: 10px; display: inline-block; }
        input { margin: 10px; }
        button { background: #e74c3c; color: white; border: none; padding: 10px 20px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="box">
        <h1>Files Uploader v1.0</h1>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file" required>
            <br>
            <button type="submit">Upload</button>
        </form>
        {% if message %}
            <p>{{ message }}</p>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return render_template_string(HTML_TEMPLATE, message="No file part")
    
    file = request.files['file']
    if file.filename == '':
        return render_template_string(HTML_TEMPLATE, message="No selected file")
    
    filename = file.filename.lower()
    
    # WEAK SECURITY FILTER
    # 1. Blocks exact ".php" but allows ".php5", ".phtml", ".PHp" (if logic was different), etc.
    # 2. Checks Content-Type but we can spoof it.
    
    # Vulnerability 1: Case sensitivity bypass (if OS is case sensitive, but here we lower() it, 
    # wait, if I lower() it, I can't bypass with .PHP. 
    # Let's make it vulnerable to double extensions or .php5
    
    blacklist = ['.php', '.exe', '.sh']
    
    # Weak check: strictly ends with
    is_blocked = False
    for ext in blacklist:
        if filename.endswith(ext):
            is_blocked = True
            break
            
    # Vulnerability 2: Double extension bypass mechanism? 
    # Actually, let's make it so it only checks the very last extension.
    # So file.php.jpg -> accepted. 
    # But usually web servers execute the first recognized extension.
    
    if is_blocked:
         return render_template_string(HTML_TEMPLATE, message="Security Alert: Extension not allowed!")

    save_path = os.path.join(UPLOAD_FOLDER, file.filename) # Preserves original case
    file.save(save_path)
    
    return render_template_string(HTML_TEMPLATE, message=f"Success! File uploaded to <a href='/uploads/{file.filename}'>/uploads/{file.filename}</a>")

if __name__ == '__main__':
    app.run(debug=True, port=5000)
