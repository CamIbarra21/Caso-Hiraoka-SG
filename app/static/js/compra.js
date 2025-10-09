document.addEventListener('DOMContentLoaded', function() {
    // Obtener elementos clave
    const qtyInput = document.getElementById('quantity-cart');
    const subtotalElement = document.querySelector('.product-subtotal');
    const subtotalFinalElement = document.getElementById('subtotal-final');
    const totalPedidoElement = document.getElementById('total-pedido');
    const minusBtn = document.getElementById('minus-qty-cart');
    const plusBtn = document.getElementById('plus-qty-cart');
    

    const productPrice = parseFloat(qtyInput.getAttribute('data-price'));
    const maxStock = parseInt(qtyInput.getAttribute('max'));

    function formatCurrency(number) {
        return number.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }


    function updateTotals() {
        let currentQty = parseInt(qtyInput.value);


        if (isNaN(currentQty) || currentQty < 1) {
            currentQty = 1;
        } else if (currentQty > maxStock) {
            currentQty = maxStock;
        }
        qtyInput.value = currentQty;
        
        const newSubtotal = productPrice * currentQty;
        
        const formattedSubtotal = formatCurrency(newSubtotal);
        

        subtotalElement.textContent = formattedSubtotal;
        

        subtotalFinalElement.textContent = formattedSubtotal;

        totalPedidoElement.textContent = formattedSubtotal; 
    }


    minusBtn.addEventListener('click', function() {
        let currentVal = parseInt(qtyInput.value);
        const minVal = parseInt(qtyInput.getAttribute('min'));
        if (currentVal > minVal) {
            qtyInput.value = currentVal - 1;
            updateTotals();
        }
    });


    plusBtn.addEventListener('click', function() {
        let currentVal = parseInt(qtyInput.value);
        if (currentVal < maxStock) {
            qtyInput.value = currentVal + 1;
            updateTotals();
        }
    });

    updateTotals();
});