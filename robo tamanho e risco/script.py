import os
import cv2
import numpy as np
from PIL import Image

def arredondar_tamanho(valor):
    base = round(valor / 100) * 100
    return max(600, min(1500, base))

def process_reference(ref_img):
    """Processa uma imagem de referência e retorna os contornos e a máscara."""
    if ref_img.shape[-1] == 4:
        alpha_channel = ref_img[:, :, 3]
        _, mask = cv2.threshold(alpha_channel, 200, 255, cv2.THRESH_BINARY)
        ref_img = ref_img[:, :, :3]
    else:
        gray = cv2.cvtColor(ref_img, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours, mask, ref_img

def process_images(input_folder, output_folder, ref_path1, ref_path2):
    os.makedirs(output_folder, exist_ok=True)
    ref_img1 = cv2.imread(ref_path1, cv2.IMREAD_UNCHANGED)
    ref_img2 = cv2.imread(ref_path2, cv2.IMREAD_UNCHANGED)
    
    if ref_img1 is None or ref_img2 is None:
        print("Erro ao carregar as imagens de referência.")
        return
    
    contours1, mask1, ref_img1 = process_reference(ref_img1)
    contours2, mask2, ref_img2 = process_reference(ref_img2)
    
    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            caminho_origem = os.path.join(input_folder, filename)
            caminho_destino = os.path.join(output_folder, filename)
            
            try:
                with Image.open(caminho_origem) as img:
                    is_png = filename.lower().endswith(".png")
                    img = img.convert("RGBA") if is_png else img.convert("RGB")
                    largura, altura = img.size
                    
                    tamanho = arredondar_tamanho(max(largura, altura))
                    fator = min(tamanho / largura, tamanho / altura)
                    nova_largura = int(largura * fator)
                    nova_altura = int(altura * fator)
                    img = img.resize((nova_largura, nova_altura), Image.LANCZOS)
                    
                    fundo = (255, 255, 255, 0) if is_png else (255, 255, 255)
                    nova_imagem = Image.new("RGBA" if is_png else "RGB", (tamanho, tamanho), fundo)
                    pos_x = (tamanho - nova_largura) // 2
                    pos_y = (tamanho - nova_altura) // 2
                    nova_imagem.paste(img, (pos_x, pos_y), img if is_png else None)
                    nova_imagem.save(caminho_destino, format="PNG" if is_png else "JPEG")
                    
                target_img = cv2.imread(caminho_destino)
                h, w, _ = target_img.shape
                positions1 = [(0, 0)]
                positions2 = [(w - 0, h - 0)]
                
                for contour in contours1:
                    x, y, w_ref, h_ref = cv2.boundingRect(contour)
                    trace = ref_img1[y:y+h_ref, x:x+w_ref]
                    trace_mask = mask1[y:y+h_ref, x:x+w_ref]
                    for px, py in positions1:
                        if px + w_ref <= w and py + h_ref <= h:
                            roi = target_img[py:py+h_ref, px:px+w_ref]
                            trace_masked = cv2.bitwise_and(trace, trace, mask=trace_mask)
                            roi_masked = cv2.bitwise_and(roi, roi, mask=cv2.bitwise_not(trace_mask))
                            blended = cv2.add(roi_masked, trace_masked)
                            target_img[py:py+h_ref, px:px+w_ref] = blended
                
                for contour in contours2:
                    trace = ref_img2[y:y+h_ref, x:x+w_ref]
                    trace_mask = mask2[y:y+h_ref, x:x+w_ref]
                    for px, py in positions2:
                        px_adjusted = px - w_ref
                        py_adjusted = py - h_ref
                        if px_adjusted >= 0 and py_adjusted >= 0:
                            roi = target_img[py_adjusted:py_adjusted+h_ref, px_adjusted:px_adjusted+w_ref]
                            trace_masked = cv2.bitwise_and(trace, trace, mask=trace_mask)
                            roi_masked = cv2.bitwise_and(roi, roi, mask=cv2.bitwise_not(trace_mask))
                            blended = cv2.add(roi_masked, trace_masked)
                            target_img[py_adjusted:py_adjusted+h_ref, px_adjusted:px_adjusted+w_ref] = blended
                
                cv2.imwrite(caminho_destino, target_img)
                print(f"Imagem processada e salva: {caminho_destino}")
            except Exception as e:
                print(f"Erro ao processar {filename}: {e}")
    
if __name__ == "__main__":
    process_images("editar", "pronto", "imagem_referencia1.jpg", "imagem_referencia2.jpg")
