import React, { useEffect, useState } from 'react';

function Jsonw() {
    
    const token = 'SEU_TOKEN_JWT_AQUI';
     
    // Divide o token nas três partes: cabeçalho, payload e assinatura
    
    const [header, payload, signature] = token.split('.');
     
    // Decodifica as partes Base64
    
    const decodedHeader = Buffer.from(header, 'base64').toString('utf-8');
    
    const decodedPayload = Buffer.from(payload, 'base64').toString('utf-8');
     
    console.log('Header decodificado:', decodedHeader);
    
    console.log('Payload decodificado:', decodedPayload);
    
    console.log('Assinatura:', signature);
    
    
     
    // Exemplo de requisição
    const apiUrl = 'http://62.72.63.140:5000/verificar_credenciais';
    const contentType = 'application/json';
     
    // Corpo da solicitação com os valores coletados, incluindo a senha da API
    const data = {
        email: 'ronaldo.lazzari@messeminvestimentos.com.br',
        senha: 'ronaldo.lazzari'
    };
     
    // Configuração da solicitação com a senha da API no cabeçalho
    const senhaAPI = 'F14C7D7625414A3E5DA1811349667';
     
    let jsonData_key; // Declare as variáveis aqui
    
     
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
        try {
            const jsonData = JSON.parse(result);
            jsonData_key = jsonData.key; // Atribua os valores aqui
            token = jsonData.token;
            // Divide o token nas três partes: cabeçalho, payload e assinatura
            const [header, payload, signature] = token.split('.');
           
            // Decodifica as partes Base64
            const decodedHeader = Buffer.from(header, 'base64').toString('utf-8');
            const decodedPayload = Buffer.from(payload, 'base64').toString('utf-8');
           
            console.log('Header decodificado:', decodedHeader);
            console.log('Payload decodificado:', decodedPayload);
         
        } catch (error) {
            console.error('Erro ao analisar JSON:', error);
        }
    })
    .catch(error => {
        console.error('Erro:', error);
    });
    return (
        alert(decodedPayload)
    );
}

export default Jsonw;
