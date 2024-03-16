<script>
    import {page} from "$app/stores";
    import {goto} from '$app/navigation';
    import {onMount} from "svelte"
    import {fillUrl, getCookie} from "$lib/utils.js"
    import {productDetailUrl, productUpdateUrl} from "$lib/config.js"
    import {supplierFilter, categoryFilter} from "$lib/stores.js"
    import ProductDetailForm from '$lib/components/ProductDetailForm.svelte'
    export let data;
    let productData = {}
    let suppliers = {}
    let categories = {}
    let formReady = true
    async function submitForm(data){
        let res = await fetch(productUpdateUrl, {
            "credentials": "include",
            "method": "PATCH",
            "body": data,
            "headers": {
                "X-CSRFToken": getCookie('csrftoken'),
            }
        })
        if(res.ok){
            goto('/inventory/list')
        }
    }

    onMount(()=>{
        formReady = false
        for (let category of $categoryFilter){
            console.log(category)
            categories[category['id']] = category['label']
        }
        for (let supplier of $supplierFilter){
            suppliers[supplier['id']] = supplier['label']
        }
        formReady = true
    })
</script>

{#if formReady}
<ProductDetailForm id={data.id} name={data.name} price={data.price} quantity={data.quantity} img={data.image} serverSubmit={submitForm} supplier_id={data.product_supplier} category_id={data.product_category} supplier={suppliers} category={categories}/>
{/if}