// App.js (ou onde as rotas são definidas)
import React from 'react';


//import About from './About';


function Dash(){
  
  async function txt() {
      const email =""
      const senha = ""
      const apiUrl = 'http://62.72.63.140:5000/all_log';
      const contentType = 'application/json';
      let jsonData_key; // Declare as variáveis aqui
      let token;
  
      
  
      const senhaAPI = 'F14C7D7625414A3E5DA1811349667';
  
      fetch(apiUrl, {
        method: 'GET',
        headers: {
          'Content-Type': contentType,
          'X-API-KEY': senhaAPI
        },
        body: JSON.stringify()
      })
        .then(response => response.text())
        .then(result => {
          try {
            const jsonData = JSON.parse(result);
            const decodedPayload = atob(jsonData.token.split('.')[1]);
            const parsedPayload = JSON.parse(decodedPayload);
            console.log(parsedPayload);
            jsonData_key = jsonData.key;
            token = jsonData.token;
            //alert(decodedPayload);

            const logData = decodedPayload // Obtém o texto do log diretamente da resposta

            // Cria um elemento 'a' para iniciar o download
            const element = document.createElement('a');
            const file = new Blob([logData], { type: 'text/plain' });
            element.href = URL.createObjectURL(file);
            element.download = 'log.txt';
            document.body.appendChild(element);
            element.click();
        
    }
    catch (error) {
      console.error('Erro:', error);
    }
    
  });



    
}
return(
  <div>
    <h2>Funfou dash</h2>
    <button onClick={txt}></button>
  </div>

  
)
}
export default Dash;
