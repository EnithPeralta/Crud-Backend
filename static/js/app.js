
function agregarProducto(){
    const producto = {
        codigo :codigo.value,
        nombre : nombre.value,
        precio : precio.value,
        categoria:cdCategoria.value
    }
    const foto = {
        foto:base64URL
    }
    const datos = {
        producto:producto,
        foto:foto
    }
    const url = "/agreagarProductoJson"
    fetch(url,{
        method:'POST',
        body:JSON.stringify(datos),
        headers:{
            "Content-Type":"application/json",
        },
    })
    .then(respuesta =>respuesta.json())
    .then(resultado =>{
        console.log(resultado)
        if (resultado.estado) {
            Formulario.reset()
            swal.fire('Agregar Producto',resultado.mensaje,"success")            
        }else{
                swal.fire('Agregar Producto',resultado.mensaje,"warning")            
        }
    })
}
async function visualizarFoto(evento) {
    const files = evento.target.files;
    const archivo = files[0];
    const filename = archivo.name;
    const extension = filename.split('.').pop().toLowerCase();
  
    try {
      if (extension !== 'jpg') {
        fileFoto.value = ""; 
        swal.fire("Seleccionar", "La imagen debe ser en formato JPG", "warning");
        return; 
      }
  
      const base64URL = await encodeFileAsBase64URL(archivo);
      const objectURL = URL.createObjectURL(archivo);
  
      imagenProducto.setAttribute("src", objectURL);
    } catch (error) {
      console.error("Error processing image:", error);
      // Handle potential errors gracefully
    }
  }
  
  /**
   * Returns a file in Base64URL format.
   * @param {File} file
   * @return {Promise<string>}
   */
  async function encodeFileAsBase64URL(file) {
    return new Promise((resolve) => {
      const reader = new FileReader();
      reader.addEventListener('loadend', () => {
        resolve(reader.result); // Resolve with Base64-encoded data
      });
      reader.readAsDataURL(file);
    });
  }

