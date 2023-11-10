const jwt = require('jsonwebtoken');
//62.72.63.140:5000
//127.0.0.1:5000
// Exemplo de requisição
const apiUrl = 'http://62.72.63.140:5000/verificar_credenciais';
const contentType = 'application/json';

//Corpo da solicitação com os valores coletados, incluindo a senha da API
const data = {
    email: "ronaldo.lazzari@messeminvestimentos.com.br",
    senha: "senha do ronaldo",
    
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

    .then(response => response.text())
    .then(result => {
        const jsonData = JSON.parse(result); // Tente analisar o JSON da resposta
        //console.log('Resposta JSON:', jsonData);
        jsonData_key = jsonData.key
        token = jsonData.token


        const decoded = jwt.decode(token, { complete: true }); // Não precisa da chave do JWT
        console.log(decoded.payload);
        //console.log(jsonData_key)
    })
    .catch(error => {
        console.error('Erro:', error);
    });