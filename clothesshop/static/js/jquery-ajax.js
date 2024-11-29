$(document).ready(function () {
    var successMessage = $("#jq-notification");

    $(document).on("click", ".add-to-cart", function (e) {
        e.preventDefault();

        var product_id = $(this).data("product-id");
        var size = $(".size-button.selected").data("size")
        if (!size) {
            alert("Please choose a size");
            return
        }
        var add_to_cart_url = $(this).attr("href");

        $.ajax({
            type: "POST",
            url: add_to_cart_url,
            data: {
                product_id: product_id,
                size: size,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 5000);

                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);

            },

            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    });

    $(document).on("click", ".size-button", function () {
        $(".size-button").removeClass("selected");
        $(this).addClass("selected");
    });


    $(document).on("click", ".remove-from-cart", function (e) {
        e.preventDefault();

        var cart_id = $(this).data("cart-id");
        var remove_from_cart = $(this).attr("href");

        $.ajax({

            type: "POST",
            url: remove_from_cart,
            data: {
                cart_id: cart_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 5000);

                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);

            },

            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    });


    $(document).on("click", ".decrement", function (e) {
        e.preventDefault();
        var cartID = $(this).data("cart-id");
        var change_cart_url = $(this).data("quantity-change-url");
        var $input = $(this).closest('.quantity-change').find('.number');
        var currentValue = parseInt($input.val());
        if (currentValue > 1) {
            $input.val(currentValue - 1);
            updateQuantity(cartID, currentValue - 1, -1, change_cart_url);
        }
    });

    $(document).on("click", ".increment", function (e) {
        e.preventDefault();
        var cartID = $(this).data("cart-id");
        var change_cart_url = $(this).data("quantity-change-url");
        var $input = $(this).closest('.quantity-change').find('.number');
        var currentValue = parseInt($input.val());

        $input.val(currentValue + 1);

        updateQuantity(cartID, currentValue + 1, 1, change_cart_url);
    });

    function updateQuantity(cartID, quantity, change, url) {
        $.ajax({
            type: "POST",
            url: url,
            data: {
                cart_id: cartID,
                quantity: quantity,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },

            success: function (data) {

                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);

            },
            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    }

    $(document).on("change", ".size-selector", function (e) {
        e.preventDefault();

        var cart_id = $(this).data("cart-id");
        var size_id = $(this).val();
        var change_size_url = $(this).data("size-change-url");

        $.ajax({
            type: "POST",
            url: change_size_url,
            data: {
                cart_id: cart_id,
                size: size_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Обновляем корзину на основе ответа
                $("#cart-items-container").html(data.cart_items_html);
            },
            error: function (data) {
                console.log("Ошибка при изменении размера в корзине");
            },
        });
    });


    $(document).on("change", ".delivery-selector", function () {
        var delivery_type = $(this).val();
        var change_delivery_url = $(this).data("change-delivery-url");

        $.ajax({
            type: "POST",
            url: change_delivery_url,
            data: {
                delivery_type: delivery_type,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                $('#delivery-price').text(data.delivery_price ? data.delivery_price + ' RUB' : 'FREE');
                $('#total-price').text(data.total_price + ' RUB');

                $("#cart-items-container").html(data.cart_html);
            },
            error: function () {
                console.log("Ошибка при обновлении доставки");
            },
        });
    });


    var notification = $('#notification');
    if (notification.length > 0) {
        setTimeout(function () {
            notification.alert('close');
        }, 5000);
    }

    // // Обработчик события радиокнопки выбора способа доставки
    // $("input[name='requires_delivery']").change(function () {
    //     var selectedValue = $(this).val();
    //     // Скрываем или отображаем input ввода адреса доставки
    //     if (selectedValue === "1") {
    //         $("#deliveryAddressField").show();
    //     } else {
    //         $("#deliveryAddressField").hide();
    //     }
    // });

    // // Форматирования ввода номера телефона в форме (xxx) xxx-хххx
    // document.getElementById('id_phone_number').addEventListener('input', function (e) {
    //     var x = e.target.value.replace(/\D/g, '').match(/(\d{0,3})(\d{0,3})(\d{0,4})/);
    //     e.target.value = !x[2] ? x[1] : '(' + x[1] + ') ' + x[2] + (x[3] ? '-' + x[3] : '');
    // });

    // // Проверяем на стороне клинта коррекность номера телефона в форме xxx-xxx-хх-хx
    // $('#create_order_form').on('submit', function (event) {
    //     var phoneNumber = $('#id_phone_number').val();
    //     var regex = /^\(\d{3}\) \d{3}-\d{4}$/;
    //
    //     if (!regex.test(phoneNumber)) {
    //         $('#phone_number_error').show();
    //         event.preventDefault();
    //     } else {
    //         $('#phone_number_error').hide();
    //
    //         // Очистка номера телефона от скобок и тире перед отправкой формы
    //         var cleanedPhoneNumber = phoneNumber.replace(/[()\-\s]/g, '');
    //         $('#id_phone_number').val(cleanedPhoneNumber);
    //     }
    // });
});