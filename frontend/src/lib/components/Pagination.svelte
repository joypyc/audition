<script>
    export let current_page;
    export let last_page;
    export let per_page;
    // export let from;
    // export let to;
    export let total;
  
    import { createEventDispatcher } from 'svelte';
  
    const dispatch = createEventDispatcher();
    let from
    let to

    function range(endAt, startAt) {
        let arr =  Array.from({ length: endAt - startAt }, (_, i) => i + startAt)
        return arr
    }

    function changePage(page) {
      if (page !== current_page) {
        dispatch('change', page);
      }
    }
    function setFrom(current_page){
        from = parseInt(current_page) * parseInt(per_page)
    }
    function setTo(current_page){
        to = last_page - (current_page * per_page)
    }
    let firstPage = 1
    let lastPage = last_page
    let reloadPagination = false
    function getRangePages(current_page){
        reloadPagination = true
        if (current_page < 5){
            firstPage = 1
        } else {
            firstPage = current_page - 4
        }
        if (lastPage > last_page){
            lastPage = last_page
        } else {
            lastPage =  current_page + 4
        }
        reloadPagination = false
        return firstPage, lastPage
    }

    $: getRangePages(current_page)
    $: setFrom(current_page)
    $: setTo(current_page)
  </script>
  
  <!-- <p>
    Page <code>{current_page}</code> of <code>{last_page}</code> (<code>{from + 1}</code> - <code>{to}</code> on <code>{total}</code> items)
  </p> -->
  
  <nav class="pagination">
    <ul>
      <li class="{current_page === 1 ? 'disabled' : ''}">
        <a href="javascript:void(0)" on:click="{() => changePage(current_page - 1)}">
          <span aria-hidden="true">«</span>
        </a>
      </li>
      {#if !reloadPagination}
      {#each range(lastPage, firstPage) as page}
      <li class='{page === current_page ? "active": ""}'>
        <a href="javascript:void(0)" on:click="{() => changePage(page)}">{page}</a>
      </li>
      {/each}
      {/if}
      <li class="{current_page === last_page ? 'disabled' : ''}">
        <a href="javascript:void(0)" on:click="{() => changePage(current_page + 1)}">
          <span aria-hidden="true">»</span>
        </a>
      </li>
    </ul>
  </nav>
  
  <style>
    .pagination {
      display: flex;
      justify-content: center;
    }
    .pagination ul {
      display: flex;
      padding-left: 0;
      list-style: none;
    }
    .pagination li a {
      position: relative;
      display: block;
      padding: .5rem .75rem;
      margin-left: -1px;
      line-height: 1.25;
      background-color: #fff;
      border: 1px solid #dee2e6;
    }
  
    .pagination li.active a {
      color: #fff;
      background-color: #007bff;
      border-color: #007bff;
    }
  
    .pagination li.disabled a {
      color: #6c757d;
      pointer-events: none;
      cursor: auto;
      border-color: #dee2e6;
    }
  </style>