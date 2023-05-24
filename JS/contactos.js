//---Validacion del formulario mediante Javascript---//

const formu = document.querySelector('#form'); //devuelve mediante el id(por eso el #) al formulario, y lo almacenamos en $formu  
const nombre = document.getElementById("inputNombre").value.trim(); //obtenemos los valores de los input por id y recortamos posibles espacios en blanco
const apellido = document.getElementById("inputApellido").value.trim();
const mail = document.getElementById("inputMail").value.trim();
const telefono = document.getElementById("inputTelefono").value.trim();

formu.addEventListener('submit', detectSubmit); //creamos un evento cuando el usuario presione el boton enviar y llamamos a la funcion detectsubmit
async function detectSubmit(event) { //la funcion detectsubmit recibe el evento
    event.preventDefault(); //preventdefault evita que se redireccione a la url del formulario al tocar el boton "enviar"
    if (formu.nombre.value === "" || formu.apellido.value === "" || formu.mail.value === "" || formu.telefono.value === "" ) { //valida que estén estos campos completos
        alert('Por favor, complete todos los campos del formulario de contacto');
        return false;
    }
    else if(isNaN(formu.telefono.value)){//isNaN verifica si solo es numérico el contenido de telefono
        alert("El campo 'telefono' solo puede contener dígitos numéricos.");
        return false;
    }
    const form = new FormData(this); //para guardar la informacion del formulario

    //la API fetch funciona para recuperar o hacer solicitud de recursos de la red
    //La llamada inicia una solicitud y devuelve una promesa. Cuando se completa la solicitud, la promesa se resuelve en el objeto de respuesta.fetch()
    const response = await fetch(this.action, { //el primer argumento es la url de la solicitud, en este caso el action del formulario
        method: this.method, body: form, headers:
            { 'Accept': 'application/json' }//Algunos servidores API pueden funcionar con múltiples formatos: JSON, XML, etc. En el encabezado especificamos que solicitamos los datos exclusivamente en formato JSON
    }) //method es el metodo HTTP para realizar la solicitud en nuestro caso es POST, el cuerpo de la solicitud HTTP y los encabezados para adjuntar en la solicitud
    if (response.ok) { //si pasa todas las validaciones aparece el comentario en pantalla con alert
        this.reset();
        alert('Gracias por contactarnos, te escribiremos a la brevedad');
    }
}
