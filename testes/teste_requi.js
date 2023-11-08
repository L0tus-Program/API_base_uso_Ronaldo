const jwt = require('jsonwebtoken');


// Ignore a função cifra, será substituida por outro metodo de criptografia

function cifra(text) {
    const shift = 22;
    let decrypted_text = "";
  
    for (let i = 0; i < text.length; i++) {
      const char = text[i];
      if (char.match(/[a-zA-Z]/)) {
        const is_upper = char === char.toUpperCase();
        char = char.toLowerCase();
        const char_code = char.charCodeAt(0);
        const decrypted_char_code = ((char_code - 'a'.charCodeAt(0) - shift + 26) % 26) + 'a'.charCodeAt(0);
        decrypted_text += is_upper ? String.fromCharCode(decrypted_char_code).toUpperCase() : String.fromCharCode(decrypted_char_code);
      } else {
        decrypted_text += char;
      }
    }
  
    return decrypted_text;
  }
  



// Exemplo de requisição
const apiUrl = 'http://127.0.0.1:5000/verificar_credenciais'; // Substitua pela URL da sua API
const contentType = 'application/json'; // Tipo de conteúdo apropriado para a sua API


// Corpo da solicitação com os valores coletados, incluindo a senha da API
const data = {
    email: 'ronaldo.lazzari@messeminvestimentos.com.br',
   
    senha: 'senha do ronaldo'
    
};

// Configuração da solicitação com a senha da API no cabeçalho
const senhaAPI = 'F14C7D7625414A3E5DA1811349667';

fetch(apiUrl, {
    method: 'POST',
    headers: {
        'Content-Type': contentType,
        'X-API-KEY': senhaAPI
    },
    body: JSON.stringify(data)
})
    .then(response => response.text()) // Altere para response.text() para obter o conteúdo da resposta como texto
    .then(result => {
        //console.log('Resposta da API:', result); // Imprima a resposta para depurar
        try {
            const jsonData = JSON.parse(result); // Tente analisar o JSON da resposta
            //console.log('Resposta JSON:', jsonData);
            jsonData_key = jsonData.key
            token = jsonData.token


           const decoded = jwt.decode(token, { complete: true }); // Não precisa da chave do JWT
           console.log(decoded.payload);
            //console.log(jsonData_key)
        } catch (error) {
            console.error('Erro ao analisar JSON:', error);
        }
    })
    .catch(error => {
        console.error('Erro:', error);
    });

