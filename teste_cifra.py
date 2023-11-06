def caesar_decipher(text):
    shift = 22
    decrypted_text = ""
    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            char = char.lower()
            char_code = ord(char)
            decrypted_char_code = ((char_code - ord('a') - shift) % 26) + ord('a') 
            if is_upper:
                decrypted_text += chr(decrypted_char_code).upper()
            else:
                decrypted_text += chr(decrypted_char_code)
        else:
            decrypted_text += char
    return decrypted_text



def caesar_cipher(text):
    shift = 22
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            char = char.lower()
            char_code = ord(char)
            encrypted_char_code = ((char_code - ord('a') + shift) % 26) + ord('a') 
            if is_upper:
                encrypted_text += chr(encrypted_char_code).upper()
            else:
                encrypted_text += chr(encrypted_char_code)
        else:
            encrypted_text += char
    return encrypted_text

# Exemplo de uso:
plaintext = "CG1hUuCabtbNY1DSBaLUOhug5KRkxS66NtNQ9N9tIAw"
#shift_amount = 22
encrypted_text = caesar_cipher(plaintext, shift_amount)
print(f"Texto original: {plaintext}")
print(f"Texto criptografado: {encrypted_text}")

decrypted_text = caesar_decipher(encrypted_text, shift_amount)

print(f"Descriptogradafo : {decrypted_text}")
