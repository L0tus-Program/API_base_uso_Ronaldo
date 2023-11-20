import React from 'react';

function Log() {
  async function handleDownload() {
    try {
      const response = await fetch('http://sua-api.com/rota-do-log');
      if (!response.ok) {
        throw new Error('Erro ao buscar o log');
      }

      const logData = await response.text(); // Obtém o texto do log diretamente da resposta

      // Cria um elemento 'a' para iniciar o download
      const element = document.createElement('a');
      const file = new Blob([logData], { type: 'text/plain' });
      element.href = URL.createObjectURL(file);
      element.download = 'log.txt';
      document.body.appendChild(element);
      element.click();
    } catch (error) {
      console.error('Erro:', error);
    }
  }

  return (
    <div className="App">
      <button onClick={handleDownload}>Baixar Log</button>
    </div>
  );
}

export default Log;