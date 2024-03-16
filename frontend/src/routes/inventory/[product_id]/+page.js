import { error } from '@sveltejs/kit';
import {productDetailUrl} from "$lib/config.js"
import {fillUrl} from "$lib/utils.js"
/** @type {import('./$types').PageLoad} */export async function load({ fetch, params }) {
    if (params.product_id) { 
        let productData = {}
        let url = fillUrl({product:  String(params.product_id)}, productDetailUrl)
        let res = await fetch(url)
        if (res.ok){
            productData = await res.json()
        }
        return productData; 
    }
    error(404, 'Not found');
}