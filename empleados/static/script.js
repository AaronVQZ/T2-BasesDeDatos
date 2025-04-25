document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-bar');
    const searchButton = document.getElementById('search-button');
    const tabla = document.getElementById('tabla_empleados');
    

    // Función para actualizar la tabla
    function actualizarTabla(empleados) {

        // Para debuggear
        console.log('Empleados:', empleados);

        // Define el encabado de la tabla
        let tableContent = `
            <tr class="encabezado">
                <th>Nombre</th>
                <th>Identificación</th>
                <th>Acciones</th>
            </tr>
        `;
        
        // Agregar las filas de empleados
        empleados.forEach(empleado => {
            tableContent += `
                <tr>
                    <td>${empleado.nombre}</td>
                    <td>${empleado.identificacion}</td>
                    <td class="acciones">
                    <button class="boton_consultar" onclick="consultarEmpleado('${empleado.identificacion}')">
                        Consultar
                    </button>
                    <button class="boton_modificar" onclick="modificarEmpleado('${empleado.identificacion}')">
                        Modificar
                    </button>
                    <button class="boton_borrar" onclick="borrarEmpleado('${empleado.identificacion}')">
                        Borrar
                    </button>
                </tr>
            `;
        });
        // Actualiza el contenido de la tabla
        tabla.innerHTML = tableContent;
    }

    // Evento para el botón de búsqueda
    searchButton.addEventListener('click', function() {
        const searchTerm = searchInput.value.trim();
        fetchEmpleados(searchTerm);
    });

    // Evento para búsqueda al dar ENTER
    searchInput.addEventListener('keyup', function(e) {
        if (e.key === 'Enter') {
            const searchTerm = this.value.trim();
            fetchEmpleados(searchTerm);
        }
    });

    // Función para obtener empleados
    function fetchEmpleados(term) {

        //actualiza el contenido la tabla con un mensaje de carga
        tabla.innerHTML = '<tr><td colspan="2">Buscando...</td></tr>';

        // Petición para buscar empleados
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
                    tabla.innerHTML = '<tr><td colspan="2">No hubo coincidencias</td></tr>';
                } else {
                    actualizarTabla(data.empleados);
                }
            } else {
                throw new Error('Formato de respuesta inválido');
            }
        })
        .catch(error => {
            console.error('Error en la búsqueda:', error);
            tabla.innerHTML = `<tr><td colspan="2">Error: ${error.message}</td></tr>`;
        });
    }
});