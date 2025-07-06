<template>
	<div class='browse-page-container flex'>
		<h1 class='browse-page-main-header'>Women Products</h1>
		<div class='filters-container'>
			<div @click='toggleFilters' class='filters-header-wrapper flex'>
				<h2 class='filters-header'>filters</h2>
				<img class='filters-menu-icon' src='@/assets/menu-icon.png'/>
			</div>
			<div :class='[isFiltersOpened ? "" : "filters-display-none"]' class='filters-container--'>
				<div class='price-filter-container'>
					<h1 class='price-filter-header'>Price</h1>
					<div class="price-input">
            <div class="field">
              <span>Min</span>
              <input type="number" class="input-min" value="0" >
            </div>
            <div class="field">
              <span>Max</span>
              <input type="number" class="input-max" value="250" >
            </div>
          </div>
          <div class="slider">
            <div class="progress"></div>
          </div>
          <div class="range-input">
            <input type="range" class="range-min" min="0" max="250" value="0" step="10">
            <input type="range" class="range-max" min="0" max="250" value="250" step="10">
          </div>
				</div>
				<div class='sizes-filter-container'>
					<h1 class='sizes-filter-header'>Sizes</h1>
					<div class='sizes-filter-boxes-container flex'>
						<div 
							v-for='i, x in shoeSizesEU' 
							:key='x' 
							@click='toggleSizeApply(i)'
							:class='[selectedSizes.indexOf(i) !== -1 && "bg-primary"]'
							class='size-box flex'>
								{{i}}
						</div>
					</div>	
				</div>
				<div class='filters-buttons-container flex'>
					<button @click='applyFilters' class='filters-apply-button button'>Apply</button>
					<button @click='clearFilters' class='filters-cancel-button button'>Clear</button>
				</div>
			</div>
		</div>
		<div class='products-container flex'>
			<h1 class='browse-page-main-header main-header-big-screen display-none'>{{$route.params.gender}} Products</h1>
			
			<router-link v-for='product in productData' :key='product.id' :to="`/product-${$route.params.gender}-${product.name}`" class='single-product-container grid'>
				<div class='product-image-wrapper-wrapper flex'>
					<div class='product-image-wrapper flex'>	
						<img class='product-image' :src="`${baseUrl}/images/${product.name}-side.png`" />
					</div>
				</div>
				<div class='product-text'>
					<h1 class='product-name'>{{product.name}}</h1>
					<h2 class='product-price'>{{product.price}}$</h2>
				</div>
			</router-link>
		</div>
	</div>
</template>
<script>
import axios from 'axios'

export default {
	name: 'browseView',
	data() {
		return {
			isFiltersOpened: false,
			shoeSizesEU: [35, 36, 37, 38, 39, 40, 41, 42, 43, 44],
			selectedSizes: [],
			appliedSizes: [],
			productData: null,
			productDataUnfiltered: null,
			baseUrl: process.env.VUE_APP_API_URL || 'http://localhost:5000',
		}
	},
	methods: {
		toggleFilters() {this.isFiltersOpened = !this.isFiltersOpened},
		toggleSizeApply(size) {
			if (this.selectedSizes.indexOf(size) === -1 ) this.selectedSizes = [...this.selectedSizes, size]
			else { this.selectedSizes = this.selectedSizes.filter(i => i !== size) }
		},
		clearFilters() {this.selectedSizes = []},
		applyFilters() {
			this.appliedSizes = this.selectedSizes;
			this.toggleFilters();

      let priceInput = document.querySelectorAll(".price-input input"),
      minPrice = parseInt(priceInput[0].value),
      maxPrice = parseInt(priceInput[1].value);

      if (this.appliedSizes.length === 0 && maxPrice === 250 && minPrice === 0) {this.productData = this.productDataUnfiltered; return}
      
      var newProductData = []
      if (maxPrice === 250 && minPrice === 0) {
        for (let product of this.productDataUnfiltered) {
          for (let size of product.sizesOnStock) {
            if (this.appliedSizes.indexOf(Number(size)) !== -1 && newProductData.indexOf(product) === -1) newProductData = [...newProductData, product]
          }
        }
        this.productData = newProductData; return
      }
      
      if (this.appliedSizes.length === 0) {
        for (let product of this.productDataUnfiltered) {
          if (product.price >= minPrice && product.price <= maxPrice) newProductData = [...newProductData, product]
        }
        this.productData = newProductData; return
      }
      

      for (let product of this.productDataUnfiltered) {
        for (let size of product.sizesOnStock) {
          if (this.appliedSizes.indexOf(Number(size)) !== -1 && newProductData.indexOf(product) === -1 && product.price >= minPrice && product.price <= maxPrice) {
            newProductData = [...newProductData, product]
          }
        }
      }
      this.productData = newProductData 

		},
		handlePriceChange(changingValue) {
			if (Number(this.minPrice) >= Number(this.maxPrice)) {
				if (changingValue === 'minPrice')	{this.minPrice = Number(this.maxPrice) - 10}
				else {this.maxPrice = Number(this.minPrice) + 10}
			}
			if (Number(this.minPrice) === -10) this.minPrice = 0;
		},
		fetchData() {
			const url = `http://127.0.0.1:5000/products/${this.$route.params.gender}`
			axios.get(url)
				.then((res) => {this.productData = res.data; this.productDataUnfiltered = res.data;})
				.catch((err) => {console.log(err)})
					.then(() => {console.log('request made')})
		},
    priceFilterSetup() {

      const rangeInput = document.querySelectorAll(".range-input input"),
      priceInput = document.querySelectorAll(".price-input input"),
      range = document.querySelector(".slider .progress");
      let priceGap = 10;
      
      priceInput.forEach(input =>{
        input.addEventListener("input", e => {
        let minPrice = parseInt(priceInput[0].value),
        maxPrice = parseInt(priceInput[1].value);
       
        if((maxPrice - minPrice >= priceGap) && maxPrice <= rangeInput[1].max){
          if (e.target.className === "input-min"){
            rangeInput[0].value = minPrice;
            range.style.left = ((minPrice / rangeInput[0].max) * 100) + "%";
          } else {
            rangeInput[1].value = maxPrice;
            range.style.right = 100 - (maxPrice / rangeInput[1].max) * 100 + "%";
          }
        }}); 
      });

      rangeInput.forEach(input =>{
        input.addEventListener("input", e =>{
        let minVal = parseInt(rangeInput[0].value),
        maxVal = parseInt(rangeInput[1].value);

        if((maxVal - minVal) < priceGap){
          if(e.target.className === "range-min"){
            rangeInput[0].value = maxVal - priceGap
          } else {
            rangeInput[1].value = minVal + priceGap;
          }
        } else {
          priceInput[0].value = minVal;
          priceInput[1].value = maxVal;
          range.style.left = ((minVal / rangeInput[0].max) * 100) + "%";
          range.style.right = 100 - (maxVal / rangeInput[1].max) * 100 + "%";
        }});
      });
    }
	},
	props: ['changeActiveNav'],
	watch:{
		$route () {
			this.changeActiveNav(this.$route.params.gender);
			this.fetchData();
		}
	},
	created() {
		this.changeActiveNav(this.$route.params.gender);
		this.fetchData();
  },
  mounted() {
    // it doesn't see the document if doesn't wait 
    setTimeout(() => {this.priceFilterSetup()}, 100)
  }
}
</script>
<style scoped>
.browse-page-container {
	background-color: var(--bg-clr-secondary);
	margin-top: 3rem;
	flex-direction: column;
	justify-content: center;
}

.browse-page-main-header {font-size: 1.8rem; width: 18.5rem; align-self: center;}
.browse-page-main-header:first-letter { text-transform: capitalize }

.filters-container {align-self: center; width: 18.5rem;}
.filters-header-wrapper {align-items: center; gap: 1rem; cursor: pointer;}
.filters-header {font-size: 1.3rem; font-weight: 500;}
.filters-menu-icon {width: 1.4rem; height: 1.48rem; margin-top: .2rem;}

.filters-container-- {background-color: var(--bg-clr-quaternary);}


.price-filter-container {}
.price-input {
  display: flex;
}
.price-input .field {}
.price-input .field input {
  max-width: 4rem;
}
.slider{
  margin-top: 1rem;
  height: 5px;
  position: relative;
  background: #ddd;
  border-radius: 5px;
}
.slider .progress {
  height: 100%;
  left: 0; right: 0;
  position: absolute;
  border-radius: 5px;
  background: #17A2B8;
}
.range-input {position: relative;}
.range-input input {
  position: absolute;
  width: 100%;
  height: 5px;
  top: -5px;
  background: none;
  pointer-events: none;
  -webkit-appearance: none;
  -moz-appearance: none;
}
input[type="range"]::-webkit-slider-thumb{
  height: 17px;
  width: 17px;
  border-radius: 50%;
  background: #17A2B8;
  pointer-events: auto;
  -webkit-appearance: none;
  box-shadow: 0 0 6px rgba(0,0,0,0.05);
}



.sizes-filter-container {}
.sizes-filter-header, .price-filter-header {font-size: 1.2rem; font-weight: 500; margin-left: .6rem;}

.sizes-filter-boxes-container {flex-wrap: wrap; gap: .5rem; justify-content: center;}
.size-box {
	width: 5rem; 
	height: 3rem; 
	justify-content: center;
	align-items: center;
	border: 2px var(--bg-clr-primary) solid;
	border-radius: 5px;
}
.size-box:hover {border: 1px black solid; padding: 1px;}

.filters-buttons-container {
	justify-content: center;
	gap: 1rem;
	margin-top: 1rem;
}
.filters-buttons-container button {
	background-color: var(--bg-clr-tertiary);
	color: white;
	width: 5rem;
}

.products-container {
	justify-content: center;
	flex-wrap: wrap;
	margin-top: 3rem;
}
.product-image-wrapper-wrapper {justify-content: center;}
.product-image-wrapper {
	border-radius: 10px;
	background-color: var(--bg-clr-primary);
	width: 18.5rem;
	height: 18.5rem;
	overflow: hidden;
	align-items: center;
}
.product-image {width: inherit;}
.product-name {
	font-size: 1.7rem;
	max-width: 18.5rem; /*product-image-wrapper width */ /*!!!!! if you change it, change this too !!!!!!*/
	color: var(--text-clr-primary);
	margin-bottom: 0;
	margin-left: .5rem;
}
.product-price {font-size: 2rem; margin-top: .5rem; margin-left: .5rem; margin-bottom: .2rem;}
@media screen and (min-width: 650px) {.product-image-wrapper {margin-left: .5rem; margin-right: .5rem;}}
@media screen and (min-width: 692px) {	
	.filters-container, .browse-page-main-header {align-self: start; margin-left: 4rem;}
}
@media screen and (min-width: 1390px) {
	.filters-container {
		background-color: var(--bg-clr-secondary);
		margin-left: initial;
		padding: 2rem;
		border-radius: 0 0 15px 15px;	
	}
	.filters-container-- {background-color: var(--bg-clr-secondary);}
	.filters-menu-icon {display: none;}
	.browse-page-container {
		background-color: var(--bg-clr-primary);
		flex-direction: initial;
		justify-content: initial;
		gap: 1rem;
	}
	.products-container {background-color: var(--bg-clr-secondary); margin-top: initial;}
	.browse-page-main-header {display: none;}
	.main-header-big-screen {
		display: block; 
		width: 100%; 
		padding: 0;
		margin-top: 3rem; 
		margin-left: 5rem; 
		padding-bottom: 2rem;
	}
}
@media screen and (max-width: 1389px) {.filters-display-none {display: none;}}
</style>
