<script>
	import {onMount} from 'svelte'
	import {searchTerm, pageSize} from '$lib/stores'
    export let columns = [];
	export let tableData = [];
    export let searchFilterData;
	export let onRowClick;
	let filteredData = []
	let columnSearchValue = {}
</script>

<div class='row'>
    <div class='col float-left'>
    <select name='pagination' class='form-control col-2' bind:value={$pageSize}>
        <option value=10>10</option>
        <option value=25>25</option>
        <option value=50>50</option>
        <option value=100>100</option>
    </select>
    <small>
        entries per page
    </small>
</div>
<div class='col float-right'>
    <input class='form-control' type='search' id='searchTable' placeholder='Search' bind:value={$searchTerm}/>
</div>
</div>
<div class='row'>
    
</div>
<table class='table'>
	<thead>
		<tr>
        {#each columns as col}
            <th>{col.label}</th>	
        {/each}
		</tr>
	</thead>
	<tbody>
		{#each tableData as row}
                <tr on:click={onRowClick(row)}>

				{#each columns as col}
					<td>{row[col.name]}</td>
				{/each}
			</tr>
		{:else}
				<p>No Data Available</p>
		{/each}
	</tbody>
</table>