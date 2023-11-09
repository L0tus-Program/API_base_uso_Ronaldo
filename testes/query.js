const jwt = require('jsonwebtoken');

// Exemplo de requisição
const apiUrl = 'http://127.0.0.1:5000/novo_contato';
const contentType = 'application/json';

//Corpo da solicitação com os valores coletados, incluindo a senha da API
const data = {
    id: "id",
    nome: "nome",
    numero: "numero",
    codClient: "codClient",
    ConfirmouWP: "ConfirmouWP",
    ConfirmaEnvio: "ConfirmaEnvio",
    enviar: "1"
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