<template>
	<div class='product-page-container'>	
		<div class='product-page-main-content'>
			<div class='product-images-container flex'>
				<div class='product-page-title'>
					<router-link class='product-type' :to="`/browse-${$route.params.gender}`">{{$route.params.gender}} Shoes</router-link>
					<h1 class='product-name'>{{$route.params.productName}}</h1>
          <p v-if="isAddedToBag" class="add-to-bag-info">Added to bag</p>
				</div>
				<div class='main-product-image-wrapper'>
					<img :src="`${baseUrl}/images/${$route.params.productName}-${imageNames.main}.png`" />
				</div>
				<div class='other-product-images-container flex'>
					<div v-for='i, x in imageNames.other' :key='x' @click='changeMainImage(i)' class='other-image-wrapper' >
						<img :src='`${baseUrl}/images/${$route.params.productName}-${i}.png`' />
					</div>
				</div>
			</div>
			<div>
				<div class='select-size-container'>
					<h2>Select Size(EU)</h2>
					<div class='size-boxes-container flex'>
						<div v-for='i, x in shoeSizesEU' :key='x' class='size-box' :class="[`${sizeClass(i)} ${i === choosenSize ? 'choosen-size' : ''}`]" @click='chooseSize(i)'>{{i}}</div>
					</div>
				</div>
				<div class='product-price-wrapper flex'>
					<button class='add-to-bag-button button' @click='addToBag'>Add to Bag</button>
					<p class='product-price'>{{productData.price}}$</p>
				</div>
			</div>
		</div>
		<div class='description-container'>
			<h1 class='description-title'>Description</h1>
			<p class='description'>Taking the classic look of heritage Nike Running into a new realm, the Nike Air Max Pre-Day brings you a fast-paced look that's ready for today's world.A true nod to the past with a design made from at least 20% recycled material by weight.</p>
		</div>
	</div>
</template>
<script>
import axios from 'axios'

export default {
	name: 'productView',
	data() {
		return {
			shoeSizesEU: [35, 36, 37, 38, 39, 40, 41, 42, 43, 44],
			imageNames: {
				main: 'side',
				other: ['single', 'top', 'back']
			},
			productData: {},
      choosenSize: null,	
      isAddedToBag: false,
			baseUrl: process.env.VUE_APP_API_URL || 'http://localhost:5000',
		}
	},
	methods: {
		changeMainImage(imgName) {
			this.imageNames.other[this.imageNames.other.indexOf(imgName)] = this.imageNames.main;
			this.imageNames.main = imgName;
		},
		getProductInfo() {
			let url = `${process.env.VUE_APP_API_URL || 'http://localhost:5000'}/products/${this.$route.params.productName}`
			axios.get(url)
				.then(res => {this.productData = res.data; console.log(res.data)})
				.catch(err => console.log(err))
					.then(() => console.log('request made'))
		},
		sizeClass(size) {
      if (this.productData.sizesOnStock && this.productData.sizesOnStock.indexOf(String(size)) !== -1) return ''
			return 'size-disabled'
		},
    chooseSize(size) {
      if (this.productData.sizesOnStock.indexOf(String(size)) === -1 || !this.productData.sizesOnStock) return
      if (this.choosenSize === size) {this.choosenSize = null; return;}
      this.choosenSize = size
    },
    addToBag() {
      if (!this.$cookies.isKey('sessionId')) {this.toggleLogin(); alert('please login first'); return}
      if (this.choosenSize === null) {alert('please choose a size first'); return}
			let url = `${process.env.VUE_APP_API_URL || 'http://localhost:5000'}/update-bag`
			let sessionId = this.$cookies.get('sessionId')
			let productName = this.$route.params.productName
			let payload = {
				sessionId: sessionId,
				productName: productName,
        size: this.choosenSize,
			}
			let config = {withCredentials: true}
			axios.post(url, payload, config)
				.then(res => {
          if (res.data.success === true) {
            this.isAddedToBag = true;
            setTimeout(() => {this.isAddedToBag = false}, 5000)
            this.increaseBagNumber()
          }
        })
				.catch(err => console.log(err))
		}
	},
	props: ['changeActiveNav', 'toggleLogin', 'increaseBagNumber'],
	created() {
		this.changeActiveNav('none');
		this.getProductInfo();
	}
}
</script>
<style scoped>
.product-page-container {
	background-color: var(--bg-clr-secondary);
	padding-bottom: 3rem;
	margin-top: 2rem;
}
.product-page-title {width: 80%; margin-top: 1rem; padding-top: 1rem;}
.product-type {text-transform: capitalize; color: var(--clr-other); font-size: 1.3rem;}
.product-name {margin-top: .5rem;	font-size: 1.5rem;}
.add-to-bag-info {
  background-color: rgba(0, 160, 0, .3);
  padding: .1rem;
  border-radius: 6px;
  width: 8rem;
  text-align: center;
  color: var(--clr-other)
}
.product-images-container {flex-direction: column; align-items: center;}
.main-product-image-wrapper {
	border-radius: 10px; 
	overflow: hidden;
	width: 80vw;
	height: 80vw;
}
.main-product-image-wrapper img {
	width: inherit;
	margin-top: -12vw;
}
.other-product-images-container {width: 80vw; justify-content: space-between; margin-top: 1rem;}
.other-image-wrapper {
	width: 25vw;
	height: 25vw;
	border-radius: 10px;
	overflow: hidden;
	cursor: pointer;
}
.other-image-wrapper:hover {border: 1px black solid; margin: -1px;}
.other-image-wrapper img {
	width: inherit;
	margin-top: -2vw;
}

.product-page-main-content > div:last-child /*second child*/ {display: flex; flex-direction: column; align-items: center;}

.select-size-container {margin-left: 1rem; width: 80vw;}
.size-boxes-container {flex-wrap: wrap; gap: 1rem; max-width: 24rem;}
.size-box {
	width: 1.8rem;
	padding: 1rem;
	border: 1px var(--bg-clr-primary) solid;
	border-radius: 10px;
	text-align: center;
  cursor: pointer;
}
.size-box:hover {border: 2px black solid; padding: calc(1rem - 4px);}
.size-disabled {background-color: var(--bg-clr-primary); cursor: default;}
.size-disabled:hover {border: 1px var(--bg-clr-primary) solid; padding: .8rem;}
.choosen-size {
  background-color: grey;
}

.product-price-wrapper {gap: 1rem; align-items: center; justify-content: center; margin-top: 1rem; width: 80vw;}
.add-to-bag-button {
	background-color: var(--bg-clr-tertiary);
	color: white;
	width: 44vw; height: 2.5rem;
	padding-top: .6rem;
	border-radius: 5px;
}
.product-price {width: 44vw; text-align: center; font-weight: 500; font-size: 1.3rem}

.description-container {margin-left: 1rem;}
.description-title {font-size: 1.3rem;}
.description {
	font-size: .95rem;
	max-width: 90vw;
	color: var(--clr-other);
}

@media screen and (min-width: 840px) {
	.product-page-main-content {display: flex; justify-content: space-around;}
	.product-page-main-content > div:last-child /*second child*/ {margin-right: 1rem;}		

	.product-type {font-size: 1.5rem;}
	.product-name {font-size: 2rem;}

	.product-images-container {align-items: initial; margin-left: 2rem;}
	.main-product-image-wrapper {width: 21rem; height: 16rem;}
	.main-product-image-wrapper img {margin-top: -5rem;}
	.other-product-images-container  {width: 21rem;}
	.other-image-wrapper {width: 6.5rem; height: 6.5rem;}
	.other-image-wrapper img {margin-top: -.8rem;}
	
	.select-size-container {margin-top: 8rem; width: initial;}
	.select-size-container h2 {font-size: 1.2rem;}
	.size-box {padding: .8rem;}

	.product-price-wrapper {flex-direction: column-reverse; margin-right: 1rem; margin-top: 6.5rem; width: initial;}
	.add-to-bag-button {width: 22rem; font-size: 1.2rem;}
	.product-price {width: initial; align-self: start;}
		
	.description-container {margin-top: 5rem;}
	.description-title {font-size: 1.5rem;}
	.description {font-size: 1.2rem;}
}

@media screen and (max-width: 1000px) {.product-page-container {width: 100vw;}}

@media screen and (min-width: 1000px) {	
	.product-page-main-content {justify-content: center; gap: 5rem;}
	.product-page-title {position: absolute; margin-top: -9rem; left: calc(5vw + 2rem);}
	
	.product-images-container {margin-top: 9rem; flex-direction: row-reverse;}
	.main-product-image-wrapper {height: 24rem;}
	.main-product-image-wrapper img {margin-top: 0;}
	.other-product-images-container {flex-direction: column; width: 8rem; margin-top: 0;}
	
}

@media screen and (min-width: 1830px) {.product-page-title {left: 16vw; }}

</style>

