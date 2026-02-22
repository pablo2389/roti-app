import React from 'react'
export default function Modal({children, open, onClose}){if(!open) return null; return <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center"><div className="bg-white p-4">{children}<button onClick={onClose}>Cerrar</button></div></div>}
