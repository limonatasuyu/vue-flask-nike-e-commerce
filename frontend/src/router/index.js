import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../components/HomeView.vue'
import BrowseView from '../components/BrowseView.vue'
import ProductView from '../components/ProductView.vue'
import BagView from '../components/BagView.vue'
import ProfileView from '../components/ProfileView.vue'
import SignUpView from '../components/SignUpView.vue'

const routes = [
	{
		path: '/',
		name: 'homeView',
		component: HomeView
	},
	{
		path: '/browse-:gender',
		name: 'browseView',
		component: BrowseView
	},
	{
		path: '/product-:gender-:productName',
    name: 'productView',
    component: ProductView
  },
	{
		path: '/bag',
		name: 'cardView',
		component: BagView 
	},
	{
		path: '/signup',
		name: 'signupView',
		component: SignUpView
	},
	{
		path: '/profile',
		name: 'profileView',
		component: ProfileView
	},
	{
		path: '/bag',
		name: 'bagView',
		component: BagView
	}
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
