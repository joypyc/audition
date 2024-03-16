import {writable} from 'svelte/store'

export let productList = writable([])
export let loggedUser = writable()
export let csrfToken = writable()
export let categoryFilter = writable()
export let supplierFilter = writable()
export let selectedFilters = writable({})
export let pageSize = writable()
export let pageNumber = writable()
export let searchTerm = writable()