const shopContent = document.getElementById("shopContent");
const verCarrito = document.getElementById("verCarrito");
const modalContainer = document.getElementById("modal-container");
const cantidadCarrito = document.getElementById("cantidadCarrito");

let carrito = [];

productos.forEach((product)=>{
    let content = document.createElement("div");
    content.className = "card";
    content.innerHTML = `
        <img src="${product.img}">
        <h3>${product.nombre}</h3>
        <p class="price">$ ${product.precio}</p>
    `;
    shopContent.append(content);

    let comprar = document.createElement("button")
    comprar.innerText = "AGREGAR";
    comprar.className = "comprar";
    content.append(comprar);

    comprar.addEventListener("click", ()=>{

        const repeat = carrito.some((repeatProduct)=> repeatProduct.id === product.id);

        if(repeat){
            carrito.map((prod)=>{
                if(prod.id === product.id){
                    prod.cantidad++
                }
            });
        }else{
            carrito.push({
                id : product.id,
                nombre : product.nombre,
                img : product.img,
                precio : product.precio,
                cantidad : product.cantidad, 
            });
        }
        
        carritoCounter();
    });
    
});

