/*
    Evento de ejecucion en la carga de la pagina
    -------------------------------------------
*/
document.addEventListener('DOMContentLoaded', function() {
  // Eliminar las comas que acompañan a los parametros de las funciones y las clases
  eliminarComas();
});


/*
    Funciones de la pagina
    ----------------------
*/

/*
Eliminar las comas que acompañana a los parametros de las funciones y las clases
*/
function eliminarComas() {
    // Obtener el elemento dt
    const dts = document.querySelectorAll('dl.py.class > dt.sig.sig-object.py');
    const dt2s = document.querySelectorAll('dl.py.method > dt.sig.sig-object.py');
  
    // Obtener los nodos hijos de dt
    let nodes = [];
    dts.forEach(dt => nodes.push(...Array.from(dt.childNodes)));
    dt2s.forEach(dt2 => nodes.push(...Array.from(dt2.childNodes)));
  
    // Filtrar los nodos de tipo texto que contienen solo una coma y un espacio
    const nodesToRemove = nodes.filter(node => {
      return node.nodeType === Node.TEXT_NODE && /^\s*,\s*$/.test(node.textContent);
    });
  
    // Eliminar los nodos de texto seleccionados
    nodesToRemove.forEach(node => node.remove());
  }