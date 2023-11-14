import React, { useState } from 'react';
import logo from './monkey.svg';
import github from './github.svg';
import './App.css';

function App() {
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');

  function reque(event) {
    event.preventDefault(); // Evita que o formulário seja enviado normalmente (recarregar a página)
    console.log("Entrou request");

    const apiUrl = 'http://62.72.63.140:5000/verificar_credenciais';
    const contentType = 'application/json';
    let jsonData_key; // Declare as variáveis aqui
    let token;

    const data = {
      email: email,
      senha: senha,
    };

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
        try {
          const jsonData = JSON.parse(result);
          const decodedPayload = atob(jsonData.token.split('.')[1]);
          const parsedPayload = JSON.parse(decodedPayload);
          console.log(parsedPayload);
          jsonData_key = jsonData.key;
          token = jsonData.token;
          //alert(decodedPayload);
          //console.log(decodedPayload.get("email"))
          /*if (decodedPayload.email === email){
            console.log(decodedPayload.email)
            console.log("logou")
            alert("Logou")
          }*/
          if (parsedPayload.email.toLowerCase() === email.toLowerCase()) {
            console.log("logou");
            alert("Logou");
          }
          
        } catch (error) {
          alert("Deu merda, senha errada");
        }
      })
      .catch(error => {
        console.error('Erro:', error);
      });
  }

  return (
    <div className="App">
      <section className="App-section">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Api OpenAAI
        </p>
        <form className='form' onSubmit={reque}>
          E-mail: <input type="text" name="nome" value={email} onChange={(e) => setEmail(e.target.value)} /><br />
          Senha: <input type="text" name="sobrenome" value={senha} onChange={(e) => setSenha(e.target.value)} /><br />
          <input type="submit" value="Enviar" />
        </form>
        <p>
          Use e abuse da API porque não tem ninguém olhando. Isso é só um teste mesmo
        </p>
        <a href='https://github.com/L0tus-Program/API_base_uso_Ronaldo' target='_blank' rel="noreferrer"><img src={github} className='icons' alt="logo" /></a>
      </section>
    </div>
  );
}

export default App;
