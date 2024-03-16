<script>
    import Pagination from '$lib/components/Pagination.svelte'
    import Datatable from '$lib/components/Datatable.svelte'
    import AlertBox from '$lib/components/AlertBox.svelte'
    import Filters from '$lib/components/Filters.svelte'
    import {onMount} from 'svelte';
    import {productList, supplierFilter, categoryFilter, selectedFilters, searchTerm, pageSize, pageNumber} from "$lib/stores.js"
    import {inventoryListUrl, inventoryFilterUrl} from "$lib/config.js"
    import {fillUrl, capitalizeWords, getValues} from '$lib/utils.js'
    import {goto} from '$app/navigation'

    let errorMsg;
    let inventoryList = []
    let columns = []
    let currentPage
    let totalPages
    let totalRecords
    let categoryOptions = []
    let supplierOptions = []

    async function showProductForm(productData){
        let productId = productData['id']
        goto(`/inventory/${productId}`)
    }

    onMount( async()=>{
        try{
            let res = await fetch(inventoryListUrl)
            if (res.ok){
                let resData = await res.json()
                let firstItem = resData['results'][0]
                totalPages = resData['total_pages']
                currentPage = resData['current_page']
                totalRecords = resData['total_records']
                let resDataKeys = Object.keys(firstItem)
                for (let key of resDataKeys){
                    columns.push({
                        "name": key,
                        "label": capitalizeWords(key)
                    })
                }
                for (let item of resData['results']){
                    let product = {}
                    for (let col of resDataKeys){
                        product[col] = item[col]
                    }
                    inventoryList.push(product)
                }
                productList.set(inventoryList)
            } else {
                productList.set([])
                throw Error("Unable to retrieve list of products.")
            }

            let filterRes = await fetch(inventoryFilterUrl)
            if (filterRes.ok){
                let filters = await filterRes.json()
                supplierOptions = getValues(filters['supplier'])
                categoryOptions = getValues(filters['category'])
                supplierFilter.set(filters['supplier'])
                categoryFilter.set(filters['category'])
            }
            else{
                supplierFilter.set(null)
                categoryFilter.set(null)
            }
        } catch (e){
            console.error(e)
    }})
    function buildQueryParams(baseUrl, queryParams){
        baseUrl = `${baseUrl}?`
        for(let [key,values] of Object.entries(queryParams)){
            for (let val of values){
                baseUrl = `${baseUrl}&${key}=${val['id']}`
            }
        }
        return baseUrl
    }
    function changePageList(e){
        pageNumber.set(e.detail)
        currentPage = e.detail
    }
    let reloadTable = false
    async function serverSideSearch(searchValue, searchFilter={}, pageNumber){
        //build url with query params
        let url = inventoryListUrl
        if(searchFilter){
            url = buildQueryParams(url, searchFilter)
        }
        if(searchValue) {
            url = `${url}&searchTerm=${searchValue}`
        }
        if(pageSize) url = `${url}&page_size=${$pageSize}`
        if(pageNumber) url = `${url}&page=${pageNumber}`
        
        let res = await fetch(url)
        if (res.ok){
            let data = await res.json()
            productList.set(data['results'])
            totalPages = data['total_pages']
            currentPage = data['current_page']
            totalRecords = data['total_records']
        } else {
            productList.set([])
        }
    }
    function resetPageNumber(){
        pageNumber.set(1)
    }
    function onPageSizeChange(pageSize){
        resetPageNumber()
        serverSideSearch($searchTerm, $selectedFilters, $pageNumber)
    }
    function onSearch(){
        resetPageNumber()
        serverSideSearch($searchTerm, $selectedFilters, $pageNumber)
    }
    $: onPageSizeChange($pageSize)
    $: serverSideSearch($searchTerm, $selectedFilters, $pageNumber)
    
</script>

{#if errorMsg}
    <AlertBox message={errorMsg}/>
{/if}

<div class='row mb-3'>
    <div class="col-md-6">
    {#if categoryOptions}
      <Filters options={categoryOptions} id='category' label='Category' selectionStore={selectedFilters}/>
      {/if}
    </div>
    <div class="col-md-6">
      {#if supplierOptions}
      <Filters options={supplierOptions} id='supplier' label='Supplier' selectionStore={selectedFilters}/>
      {/if}
    </div>
</div>
<div class='row'>
{#if $productList && columns.length}
<Datatable columns={columns} tableData={$productList} searchFilterData={serverSideSearch} onRowClick={showProductForm}/>
<Pagination current_page={currentPage} total={totalRecords} last_page={totalPages} per_page={$pageSize} on:change={changePageList}/>
{:else}
<h2>No products available</h2>
{/if}
</div>
