document.addEventListener('DOMContentLoaded', function() {
    const qtyInput = document.getElementById('quantity');
    const minusBtn = document.getElementById('minus-qty');
    const plusBtn = document.getElementById('plus-qty');
    const hiddenQtyInput = document.getElementById('quantity_to_send');
    const maxVal = parseInt(qtyInput.getAttribute('max'));
    const minVal = parseInt(qtyInput.getAttribute('min'));
    
    function updateHiddenQuantity() {
        if (hiddenQtyInput) {
            hiddenQtyInput.value = qtyInput.value;
        }
    }


    if (plusBtn) {
        plusBtn.addEventListener('click', function() {
            let currentVal = parseInt(qtyInput.value);
            if (currentVal < maxVal) {
                qtyInput.value = currentVal + 1;
                updateHiddenQuantity();
            }
        });
    }


    if (minusBtn) {
        minusBtn.addEventListener('click', function() {
            let currentVal = parseInt(qtyInput.value);
            if (currentVal > minVal) {
                qtyInput.value = currentVal - 1;
                updateHiddenQuantity();
            }
        });
    }

    updateHiddenQuantity(); 
});