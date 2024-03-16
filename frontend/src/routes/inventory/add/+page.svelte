<script>
    import {onMount} from 'svelte'
    import ProductDetailForm from "$lib/components/ProductDetailForm.svelte"
    import AlertBox from "$lib/components/AlertBox.svelte"
    import {productAddUrl, inventoryFilterUrl} from "$lib/config.js"
    import {supplierFilter, categoryFilter} from "$lib/stores.js"
    import {getValues, getCookie} from "$lib/utils.js"
    let errorMsg = '';
    let formReady = true
    let categoryOptions = []
    let supplierOptions = []
    let suppliers = {}
    let categories = {}
    async function submitForm(data){
        try{
            let res = await fetch(productAddUrl, {
                "credentials": "include",
                "method": "POST",
                "body": data,
                "headers": {
                    "X-CSRFToken": getCookie('csrftoken'),
                }
            })
        } catch (e){
            console.log(e)
            errorMsg = e
        }
    }
    onMount(async()=>{
        formReady = false
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
        for (let category of $categoryFilter){
            categories[category['id']] = category['label']
        }
        for (let supplier of $supplierFilter){
            suppliers[supplier['id']] = supplier['label']
        }
        formReady = true
    })
</script>
{#if errorMsg}
<AlertBox message={errorMsg}/>
{/if}
{#if formReady}
<ProductDetailForm serverSubmit={submitForm} supplier={suppliers} category={categories}/>
{/if}