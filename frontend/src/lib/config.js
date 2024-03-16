const backendUrl = 'http://localhost:8000';

export const checkAuthUrl = `${backendUrl}/auth/authenticate`
export const loginUrl = `${backendUrl}/auth/login`
export const logoutUrl = `${backendUrl}/auth/logout`
export const csrfUrl = `${backendUrl}/auth/csrftoken`
export const inventoryListUrl = `${backendUrl}/api/inventory`
export const inventoryFilterUrl = `${backendUrl}/api/filters`
export const productDetailUrl = `${backendUrl}/api/inventory/{product}`
export const productUpdateUrl = `${backendUrl}/api/update-inventory`
export const productAddUrl = `${backendUrl}/api/add-inventory`
export const productDeleteUrl = `${backendUrl}/api/delete-inventory`
