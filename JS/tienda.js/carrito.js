const pintarCarrito = ()=>{
    modalContainer.innerHTML = "";
    modalContainer.style.display = "flex";

    const modalHeader = document.createElement("div");
    modalHeader.className = "modal-header";
    modalHeader.innerHTML = `
    <h1 class = "modal-header-title">DETALLE DEL PEDIDO</h1>
    `;
    modalContainer.append(modalHeader);

    const modalbutton = document.createElement("h1");
    modalbutton.innerText = "X";
    modalbutton.className = "modal-header-button";

    modalbutton.addEventListener("click", ()=>{
        modalContainer.style.display = "none";
    });

    modalHeader.append(modalbutton);

    carrito.forEach((product)=>{
        let carritoContent = document.createElement("div")
        carritoContent.className = "modal-content"
        carritoContent.innerHTML = `
            <img src="${product.img}">
            <h3>${product.nombre}</h3>
            <p>$ ${product.precio}</p>
            <p>Cantidad: ${product.cantidad}</p>
            <p>Total: $ ${product.cantidad * product.precio}</p>
            <span class="delete-product">✖</span>
        `;
    modalContainer.append(carritoContent); 

        let eliminar = carritoContent.querySelector(".delete-product");
        eliminar.addEventListener("click", ()=>{
            eliminarProducto(product.id);
        })
    
    });

    const total = carrito.reduce((acc, el)=> acc + el.precio * el.cantidad, 0);

    const totalCompra = document.createElement("div");
    totalCompra.className = "total-content";
    totalCompra.innerHTML = `Total: $ ${total}
    `;
    modalContainer.append(totalCompra);
    
  let pagarCompra= document.createElement("button")
  pagarCompra.innerText = "Finalizar compra";
  pagarCompra.className = "pagar-button";
modalContainer.append(pagarCompra);

pagarCompra.addEventListener("click", () =>{
  Swal.fire({
    icon: 'success',
    title: 'Tu compra ha sido realizada con éxito',
    text: '',
    footer: '<a href="../index.html">Ir a la tienda</a>'
  });
});
};  

verCarrito.addEventListener("click", pintarCarrito);

const eliminarProducto = (id)=>{
    const foundId = carrito.find((element) => element.id === id);

    carrito = carrito.filter((carritoId) =>{
        return carritoId !== foundId;
    });
    carritoCounter();
    pintarCarrito();
};

const carritoCounter = ()=>{
    cantidadCarrito.style.display="block";
    cantidadCarrito.innerText = carrito.length;
};



