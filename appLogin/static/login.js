// Esperar a que el DOM esté cargado
document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("login-form");
    const errorContainer = document.getElementById("error-container");
    errorContainer.innerText = ""; // Limpiar mensajes de error previos
    
    
    form.onsubmit = function(event) {

        event.preventDefault(); // Evitar que se recargue la página
        
        // Capturar los valores ingresados
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        // Validar datos antes de enviarlos
        if (!username || !password) {
            errorContainer.innerText = "Por favor, complete todos los campos.";
            errorContainer.style.display = "block"; // Mostrar el contenedor de error
            return;
        }else{
            errorContainer.style.display = "none"; // Ocultar el contenedor de error
        }
        //linea de prueba
        console.log("Datos enviados:", { username, password });


        // se crea un objeto JSON con los datos del formulario
        const jsonData = {
            username: username,
            password: password
        };
        
        // Enviar datos al servidor como JSON
        fetch("/login/", { 
            method: "POST",
            body: JSON.stringify(jsonData),
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCSRFTOKEN(),
                "Content-Type": "application/json",
                'Accept': 'application/json'
            },

        })
        .then((response) => {
            if (!response.ok) {
                return response.json().catch(() => {
                    throw new Error("Error de red o respuesta no válida.");
                });
            }
            return response.json();
        })
        .then((data) => {
            // Manejar la respuesta del servidor
            if (data.success) {
                // Show success message and redirect
                //alert(`Bienvenido, ${data.username}`);
                Swal.fire({
                    title: 'Bienvenido',
                    text: `Bienvenido, ${data.username}`,
                    icon: 'success',
                    timer: 2000,
                    showConfirmButton: false,
                    allowOutsideClick: false,
                    didOpen: () => {
                        setTimeout(() => {
                            window.location.href = data.redirect; // Redirigir a la URL proporcionada    
                        }, 2000); // 2 segundos
                    },
                });
                
            } else {
                Swal.fire({
                    title: 'Error',
                    text: data.message || "Ocurrió un error inesperado.",
                    icon: 'error',
                    timer: 2000,
                    showConfirmButton: false,
                    allowOutsideClick: false
                });
            }
        })
        .catch((error) => {
            print("catch error");
            // mostrar el error en el contenedor de error
            errorContainer.style.display = "block"; // Mostrar el contenedor de error
            errorContainer.innerText = error.message || "Ocurrió un error inesperado.";
            console.error("Login error:", error);
        })
    }
    
    function getCSRFTOKEN() {
    const token = document.querySelector("[name=csrfmiddlewaretoken]");
    if (!token) {
        console.error("CSRF token not found");
        throw new Error("CSRF token not found");
    }
    return token.value;
}

    

})
