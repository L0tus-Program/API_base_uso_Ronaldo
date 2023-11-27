// Exemplo de requisição
const apiUrl = 'https://chat.conexaoia.digital/desabilita_cliente'; // Substitua pela URL da sua API
const contentType = 'application/json'; // Tipo de conteúdo apropriado para a sua API

// Corpo da solicitação com os valores coletados, incluindo a senha da API
const data = {
  codClient: "89994"
};

// Configuração da solicitação com a senha da API no cabeçalho
const senhaAPI = 'F14C7D7625414A3E5DA1811349667';

fetch(apiUrl, {
  method: 'POST',
  headers: {
    'Content-Type': contentType,
    'X-API-KEY': senhaAPI
  },
  body: JSON.stringify(data) // Enviar o objeto data como JSON
})
  .then(response => response.text()) // Altere para response.text() para obter o conteúdo da resposta como texto
  .then(result => {
    console.log(result)
    token = result
    // Seu código de processamento da resposta aqui
    const [, payloadEncoded] = token.split('.');
  const payloadDecoded = Buffer.from(payloadEncoded, 'base64').toString('utf-8');
  console.log('Conteúdo do Payload:', payloadDecoded);
  })
  .catch(error => {
    console.error('Erro:', error);
  });
