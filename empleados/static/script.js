document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-bar');
    const searchButton = document.getElementById('search-button');
    const tabla = document.getElementById('tabla-empleados');
    //const tabla = document.querySelector('.tabla tbody') || document.querySelector('.tabla');

    // Función para actualizar la tabla
    function updateTable(empleados) {
        console.log('Empleados:', empleados);
        // Mantener el encabezado
        let tableContent = `
            <tr class="encabezado">
                <th>Nombre</th>
                <th>Identificación</th>
            </tr>
        `;
        
        // Agregar las filas de empleados
        empleados.forEach(empleado => {
            tableContent += `
                <tr>
                    <td>${empleado.nombre}</td>
                    <td>${empleado.identificacion}</td>
                </tr>
            `;
        });
        
        //tabla.innerHTML = tableContent;
    }

    // Evento para el botón de búsqueda
    searchButton.addEventListener('click', function() {
        const searchTerm = searchInput.value.trim();
        fetchEmpleados(searchTerm);
    });

    // Evento para búsqueda al escribir
    searchInput.addEventListener('keyup', function(e) {
        if (e.key === 'Enter') {
            const searchTerm = this.value.trim();
            fetchEmpleados(searchTerm);
        }
    });

    // Función para obtener empleados
    function fetchEmpleados(term) {
        //tabla.innerHTML = '<tr><td colspan="2">Buscando...</td></tr>';

        fetch(`/home/buscar-empleados/?term=${encodeURIComponent(term)}`, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error del servidor: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if ( data.success && Array.isArray(data.empleados)) {
                if (data.empleados.length === 0) {
                    console.log('No se encontraron empleados');
                } else {
                    updateTable(data.empleados);
                }
            } else {
                throw new Error('Formato de respuesta inválido');
            }
        })
        .catch(error => {
            console.error('Error en la búsqueda:', error);
            //tabla.innerHTML = `<tr><td colspan="2">Error: ${error.message}</td></tr>`;
        });
    }
});