var ctx = document.getElementById('salesChart').getContext('2d');
      var fechas = {{ fechas|safe }};
      var montos = {{ montos|safe }};
      
      var data = {
          labels: fechas,
          datasets: [{
              label: 'Ventas',
              data: montos,
              fill: false, // No rellenar el área bajo la línea
              borderColor: 'rgba(75, 192, 192, 1)', // Color de la línea
              borderWidth: 2 // Ancho de la línea
          }]
      };
      
      var config = {
          type: 'line',
          data: data,
          options: {
              scales: {
                  y: {
                      beginAtZero: true
                  }
              }
          }
      };
      
      var myChart = new Chart(ctx, config);