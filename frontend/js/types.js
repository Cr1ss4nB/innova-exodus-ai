/**
 * @typedef {Object} DocumentRecord
 * @property {string} document_id
 * @property {string} filename
 * @property {string} upload_date
 * @property {number} total_pages
 * @property {number} total_chunks
 * @property {number} size_bytes
 */

/**
 * @typedef {Object} SourceReference
 * @property {string} document
 * @property {number} page
 */

/**
 * @typedef {Object} ChatHistoryTurn
 * @property {string} question
 * @property {string} answer
 */

/**
 * @typedef {Object} ChatMessage
 * @property {string} id
 * @property {'user'|'assistant'|'error'} role
 * @property {string} text
 * @property {SourceReference[]} [sources]
 */

/**
 * @typedef {Object} ApiError
 * @property {string} detail
 * @property {string} [error_type]
 */

export {};
