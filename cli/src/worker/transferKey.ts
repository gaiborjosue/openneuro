import * as base64 from "std/encoding/base64.ts"

/** Deno port of transferKey from Node.js CLI */
interface TransferKeyState {
  // Base URL
  url: string
  // Basic auth token for repos
  token: string
}

/**
 * Create a Request object for this url and key
 * @param {object} state
 * @param {string} state.url Base URL
 * @param {string} state.token Basic auth token for repos
 * @param {string} key git-annex key
 * @param {object} options fetch options
 * @returns {Request} Configured fetch Request object
 */
export function keyRequest(state: TransferKeyState, key: string, options) {
  const headers = new Headers(
    "headers" in options && options.headers || undefined,
  )
  headers.set(
    "Authorization",
    "Basic " + base64.encodeBase64(`openneuro-cli:${state.token}`),
  )
  const requestUrl = `${state.url}/annex/${key}`
  return new Request(requestUrl, { ...options, headers })
}

/**
 * Call POST to upload a key to a remote
 * @param {object} state
 * @param {string} state.url Base URL
 * @param {string} state.token Basic auth token for repos
 * @param {string} key Git-annex key
 * @param {string} file File path
 */
export async function storeKey(state: TransferKeyState, key: string, file) {
  const fileHandle = await Deno.open(file)
  const fileStat = await fileHandle.stat()
  const requestOptions = {
    method: "POST",
    headers: {
      "Content-Length": fileStat.size,
    },
  }
  const request = keyRequest(state, key, requestOptions)
  const response = await fetch(request, { body: fileHandle.readable })
  if (response.status === 200) {
    return fileStat.size
  } else {
    return -1
  }
}

/**
 * Call GET to download a key from a remote
 * @param {object} state
 * @param {string} state.url Base URL
 * @param {string} state.token Basic auth token for repos
 * @param {string} key Git-annex key
 * @param {string} file File path
 */
export async function retrieveKey(state: TransferKeyState, key: string, file) {
  try {
    const request = keyRequest(state, key, { method: "GET" })
    const response = await fetch(request)
    if (response.status === 200 && response.body) {
      const fileHandle = await Deno.open(file, { write: true, create: true })
      await response.body.pipeTo(fileHandle.writable)
      return true
    } else {
      return false
    }
  } catch (err) {
    console.error(err)
    return false
  }
}

/**
 * Call HEAD to check if key exists on remote
 * @param {object} state
 * @param {string} state.url Base URL
 * @param {string} state.token Basic auth token for repos
 * @param {string} key
 * @returns {Promise<boolean>} True or false if key exists
 */
export async function checkKey(state: TransferKeyState, key: string) {
  const request = keyRequest(state, key, { method: "HEAD" })
  const response = await fetch(request)
  if (response.status === 200) {
    return true
  } else {
    return false
  }
}

/**
 * Call DELETE to remove a key from the remote
 * @param {object} state
 * @param {string} state.url Base URL
 * @param {string} state.token Basic auth token for repos
 * @param {string} key
 * @returns {Promise<boolean>} True or false if key exists
 */
export async function removeKey(state: TransferKeyState, key: string) {
  const request = keyRequest(state, key, { method: "DELETE" })
  const response = await fetch(request)
  if (response.status === 204) {
    return true
  } else {
    return false
  }
}
