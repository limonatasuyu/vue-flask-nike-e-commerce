<template>
	<div v-if='userData' class='page-container flex'>
		<div v-if='products.length === 0' class='product-cards-container' style='background-color: white;'>
			<p style='text-align: center; font-size: 1.4rem;'>There is nothing in here</p>
		</div>
		<div v-if='products.length > 0' class='product-cards-container'>
			<div class='card-headers flex'>
				<div>Product</div>
				<p>Name</p><p>Price</p><p>Size</p>
				<div></div>
			</div>
			<div v-for='i, x in products' :key='x' class='product-card-container flex'>
				<div class='product-image-wrapper'>
					<img class='product-image' :src="`http://localhost:5000/images/${i.name}/side.png`" />
				</div>
				<p class='product-name'>{{i.name}}</p>
				<p class='product-price'>{{i.price}}$</p>
				<p class='product-price'>{{rawProductData.length > 0 && rawProductData[x].size}}</p>
				<img class='x-icon' src='@/assets/x-icon.png' @click='deleteFromBag(i.id, rawProductData[x].size)'>
			</div>
		</div>
		<div class='checkout-section'>
			<p class='total-price grid'><span>Total:</span><span>${{totalPrice}}</span></p>
			<button class='button checkout-button'>Check Out</button>
		</div>
	</div>
</template>
<script>
import axios from 'axios'

export default {
	name: 'cardView',
	data() {
		return {
			products: [],
			totalPrice: 0,
      rawProductData: null,
		}
	},
	props:['changeActiveNav', 'userData', 'getUserInfo', 'decreaseBagNumber'],
	methods: {
		getProducts() {
			let url = 'http://localhost:5000/products-in-bag'
			let sessionId = this.$cookies.get('sessionId')
			let payload = {sessionId: sessionId}
			let config = {withCredentials: true}
			axios.post(url, payload, config)
        .then(res => this.rawProductData = res.data.product_data)
        .catch(err => console.log(err))
		},
		getProductsInfo() {
      if (this.rawProductData.length === 0) {this.products = []; return}
      let productIds = []
      for (let i of this.rawProductData) {productIds = [...productIds, i.id]}
			let url = `http://localhost:5000/products/${productIds.toString()}`
			axios.get(url)
				.then(res => this.products = res.data)
				.catch(err => console.log(err))
		},
		calculateTotalPrice() {
			if (this.products.length <= 0) return
			let totalPrice = 0
			for (let i of this.products) {totalPrice += i.price}
			this.totalPrice = totalPrice;
		},
		deleteFromBag(id, size) {
			let sessionId = this.$cookies.get('sessionId')
      let payload = {'sessionId': sessionId, 'productId': id, 'size': size}
			let config = {withCredentials: true}
			let options = {data: payload, config: config}
			axios.delete('http://localhost:5000/update-bag', options)
				.then(res => {
					console.log(res)
					if (res.data.success === true) {
						this.getProducts()
						this.decreaseBagNumber()
					}
				})
				.catch(err => console.log(err))
		}
	},
	mounted() {
		this.changeActiveNav('bag')
    this.getProducts()
	},
	watch: {
		products() {this.calculateTotalPrice()},
    rawProductData() {this.getProductsInfo()}
  }
}
</script>


<style scoped>
.page-container {gap: 1rem;}
.product-cards-container {width: 100%;}
.card-headers {
	align-items: center;
	justify-content: space-between;
	width: 100%;
	margin-top: 2rem; 
	background-color: var(--bg-clr-secondary);
	border-radius: 5px;
}
.card-headers div:first-child {margin-left: 2rem; width: 13rem}
.card-headers div:last-child {width: 1.5rem; margin-right: 5rem}
.product-card-container {
	align-items: center; 
	justify-content: space-between;
	background-color: var(--bg-clr-secondary);
	height: 8rem;
	width: 100%;
	border-radius: 5px;
	margin-top: 1rem;	
}
.product-image-wrapper {height: 6rem; overflow: hidden; margin-left: 2rem;}
.product-image {max-width: 12rem; margin-top: -5rem;}
.product-name {width: 10rem;}
.product-price {margin-left: -6rem;}

.x-icon {height: 1.5rem; width: 1.5rem; cursor: pointer; margin-right: 5rem;}

.checkout-section {
	justify-content: flex-end;
	margin-top: 1rem;
	border: 1px var(--bg-clr-tertiary) solid;
	border-radius: 10px;
	padding: 1rem;
	height: 12rem;
	background-color: var(--bg-clr-secondary);
	margin-top: 2rem;
}	
.total-price {gap: 1rem;}
.total-price span:first-child {margin-left: .5rem; font-weight: 500;}
.total-price span:last-child {justify-self: center; font-size: 2rem; font-weight: 500;}
.checkout-button {
	background-color: var(--bg-clr-tertiary);
	color: white;
	font-size: 1rem;
	margin-top: 1rem;
	width: 7rem;
}
@media screen and (max-width: 900px) {
	.page-container {flex-direction: column;}
	.checkout-section {display: flex; height: 5rem; justify-content: space-between;}
	.checkout-button {height: 3rem;}
	.total-price {display: flex; align-items: center;}
	.total-price span {font-size: 1.5rem; font-weight: 500;}
}
@media screen and (max-width: 660px) {
	.card-headers div:first-child {width: 31vw;}
	.card-headers div:last-child {margin-right: 1.5rem;}
	.product-image-wrapper {height: 15vw;}
	.product-image {height: 38vw; margin-top: -13vw;}	
	.x-icon {margin-right: 1.5rem;}
}
@media screen and (max-width: 400px) {
	.card-headers {display: none;}
	.product-card-container {justify-content: initial; gap: 10vw;}
	.product-image-wrapper {height: 4rem; margin-left: 1rem;}
	.product-image {height: 9.5rem; margin-top: -3rem;}
	.product-price {position: absolute; right: 3rem; margin-top: 7rem;}
	.x-icon {position: absolute; margin-top: -3.9rem; margin-right: 0; right: .5rem;}
	.total-price {gap: 1rem;}
	.total-price span:last-child, .total-price span:first-child {font-size: 1rem;}
}
</style>
