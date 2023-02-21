$(document).ready(function(){
	$("#loadMore").on('click', function(){
		var _currentProducts = $(".product-box").length;
		var _limit = $(this).attr('data-limit');
		var _total = $(this).attr('data-total');

		// Start Ajax
		$.ajax({
			url:'/load-more-data',
			data:{
				limit: _limit,
				offset: _currentProducts
			},
			dataType:'json',
			beforeSend:function(){
				$("#loadMore").attr('disabled',true);
				$(".load-more-icon").addClass('fa-spin');
			},
			success:function(res){
				$("#filteredProducts").append(res.data);
				$("#loadMore").attr('disabled',false);
				$(".load-more-icon").removeClass('fa-spin');

				var _totalShowing = $(".product-box").length;
				if(_totalShowing==_total){
					$("#loadMore").remove();
				}
			}
		});
		// End
	});



	$("#loadMoreCat").on('click', function () {
		var _currentProducts = $(".product-box").length;
		var _limit = $(this).attr('data-limit');
		var _total = $(this).attr('data-total');

		// Start Ajax
		$.ajax({
			url:'/load-more-dataCat',
			data:{
				limit: _limit,
				offset: _currentProducts
			},
			dataType:'json',
			beforeSend:function(){
				$("#loadMoreCat").attr('disabled',true);
				$(".load-more-icon").addClass('fa-spin');
			},
			success:function(res){
				$("#categoryProducts").append(res.data);
				$("#loadMoreCat").attr('disabled',false);
				$(".load-more-icon").removeClass('fa-spin');

				var _totalShowing = $(".product-box").length;
				if(_totalShowing==_total){
					$("#loadMoreCat").remove();
				}
			}
		});
		// End
	});


	// Добавить в корзину
	$(document).on('click', ".add-to-cart", function(){
		var _vm=$(this);
		var _index = _vm.attr('data-index');
		var _qty = $(".product-qty-"+_index).val();
		var _productId = $(".product-id-"+_index).val();
		var _productTitle = $(".product-title-"+_index).val();
		var _productImage = $(".product-image-"+_index).val();
		var _productPrice = $(".product-price-"+_index).text();
		var _productSlug = $(".product-slug-"+_index).val();
		console.log(_productTitle, _productPrice)
		// Ajax
		$.ajax({
			url:'/add-to-cart',
			data:{
				'qty':_qty,
				'id':_productId,
				'title':_productTitle,
				'image':_productImage,
				'price':_productPrice,
				'slug':_productSlug,
			},
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled', true);
			},
			success:function(res){
				$(".cart-list").text(res.totalitems);
				_vm.attr('disabled',false);
			}
		});
		// End
	});
	// End

	// Удалить товар из карзины
	$(document).on('click','.delete-item',function(){
		var _pId=$(this).attr('data-item');
		var _vm=$(this);
		// Ajax
		$.ajax({
			url:'/delete-from-cart',
			data:{
				'id':_pId,
			},
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
				$(".cart-list").text(res.totalitems);
				_vm.attr('disabled',false);
				$("#cartList").html(res.data);
			}
		});
		// End
	});

	// Update item from cart
	$(document).on('click','.update-item',function(){
		var _pId=$(this).attr('data-item');
		var _pQty=$(".product-qty-"+_pId).val();
		var _vm=$(this);
		// Ajax
		$.ajax({
			url:'/update-cart',
			data:{
				'id':_pId,
				'qty':_pQty
			},
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
				// $(".cart-list").text(res.totalitems);
				_vm.attr('disabled',false);
				$("#cartList").html(res.data);
			}
		});
		// End

	// Update item from cart
	$(document).on('click','.update-item',function(){
		var _pId=$(this).attr('data-item');
		var _pQty=$(".product-qty-"+_pId).val();
		var _vm=$(this);
		// Ajax
		$.ajax({
			url:'/update-cart',
			data:{
				'id':_pId,
				'qty':_pQty
			},
			dataType:'json',
			beforeSend:function(){
				_vm.attr('disabled',true);
			},
			success:function(res){
				// $(".cart-list").text(res.totalitems);
				_vm.attr('disabled',false);
				$("#cartList").html(res.data);
			}
		});
		// End
		});
	});

	// Product Review Save
	$("#addForm").submit(function(e){
		$.ajax({
			data:$(this).serialize(),
			method:$(this).attr('method'),
			url:$(this).attr('action'),
			dataType:'json',
			success:function(res){
				if(res.bool==true){
					$(".ajaxRes").html('Данные были добавлены.');
					$("#reset").trigger('click');
					// Скрыть кнопку
					$(".reviewBtn").hide();
					//End

					var _html = '<blockquote class="blockquote text-right">';
					_html += '<small>'+res.data.review_text+'</small>';
					_html += '<footer class="blockquote-footer">'+res.data.user;
					_html += '<cite title="Source Title">';
					for(var i=1; i<=res.data.review_rating; i++) {
						_html += '<i class="fa fa-star text-warning"></i>';
					}
					_html += '</cite>';
					_html += '</footer>';
					_html += '</blockquote>';
					_html += '<hr>';

					$(".no-data").hide();

					$(".review-list").prepend(_html);

					$("#productReview").modal('hide');

					//Средний рейтинг
					$(".avg_rating").text(res.avg_reviews.avg_rating.toFixed(1))
				}
			}
		});
		e.preventDefault();
	});
	// Product Review Save end

});