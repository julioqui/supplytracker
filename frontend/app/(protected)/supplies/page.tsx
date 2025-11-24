'use client'

import { useState, useEffect } from 'react'
import { Plus, Pencil, Trash2 } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { getAuthToken } from '@/lib/auth'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'

// Types
type Unit = 'g' | 'kg' | 'ml' | 'l' | 'un'

interface Supply {
  id: string
  name: string
  unit: Unit
  cost_per_unit: number
  stock_quantity: number
  min_stock: number
  category?: string
  created_at?: string
  updated_at?: string
}

// API functions
const API_URL = 'http://localhost:8000/api/v1'

async function getAuthHeaders() {
  const token = await getAuthToken()
  return {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {})
  }
}

async function getSupplies(): Promise<Supply[]> {
  const headers = await getAuthHeaders()
  const response = await fetch(`${API_URL}/supplies/`, {
    headers,
    credentials: 'include'
  })
  if (!response.ok) {
    throw new Error('Failed to fetch supplies')
  }
  return response.json()
}

async function createSupply(supply: Omit<Supply, 'id'>): Promise<Supply> {
  const headers = await getAuthHeaders()
  const response = await fetch(`${API_URL}/supplies/`, {
    method: 'POST',
    headers,
    credentials: 'include',
    body: JSON.stringify(supply),
  })
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'Failed to create supply')
  }
  return response.json()
}

async function updateSupply(id: string, supply: Partial<Supply>): Promise<Supply> {
  const headers = await getAuthHeaders()
  const response = await fetch(`${API_URL}/supplies/${id}`, {
    method: 'PATCH',
    headers,
    credentials: 'include',
    body: JSON.stringify(supply),
  })
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'Failed to update supply')
  }
  return response.json()
}

async function deleteSupply(id: string): Promise<void> {
  const headers = await getAuthHeaders()
  const response = await fetch(`${API_URL}/supplies/${id}`, {
    method: 'DELETE',
    headers,
    credentials: 'include',
  })
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'Failed to delete supply')
  }
}

export default function SuppliesPage() {
  const [supplies, setSupplies] = useState<Supply[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [isDialogOpen, setIsDialogOpen] = useState(false)
  const [editingSupply, setEditingSupply] = useState<Supply | null>(null)
  const [formData, setFormData] = useState({
    name: '',
    category: '',
    unit: 'un' as Unit,
    cost_per_unit: '',
    stock_quantity: '',
    min_stock: '0',
  })

  const fetchSupplies = async () => {
    try {
      setLoading(true)
      const data = await getSupplies()
      setSupplies(data)
    } catch (error) {
      console.error('Failed to fetch supplies:', error)
      // Handle error (e.g., show toast notification)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchSupplies()
  }, [])

  const handleDelete = async (id: string) => {
    if (window.confirm('Tem certeza que deseja excluir este insumo?')) {
      try {
        await deleteSupply(id)
        setSupplies(supplies.filter(supply => supply.id !== id))
      } catch (error) {
        console.error('Failed to delete supply:', error)
        // Handle error
      }
    }
  }

  const handleOpenDialog = (supply?: Supply) => {
    if (supply) {
      setEditingSupply(supply)
      setFormData({
        name: supply.name,
        category: supply.category || '',
        unit: supply.unit,
        cost_per_unit: supply.cost_per_unit.toString(),
        stock_quantity: supply.stock_quantity.toString(),
        min_stock: supply.min_stock.toString(),
      })
    } else {
      setEditingSupply(null)
      setFormData({
        name: '',
        category: '',
        unit: 'un',
        cost_per_unit: '',
        stock_quantity: '',
        min_stock: '0',
      })
    }
    setIsDialogOpen(true)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    const supplyData = {
      name: formData.name,
      category: formData.category || undefined,
      unit: formData.unit,
      cost_per_unit: parseFloat(formData.cost_per_unit),
      stock_quantity: parseFloat(formData.stock_quantity),
      min_stock: parseFloat(formData.min_stock) || 0,
    }

    try {
      if (editingSupply) {
        const updatedSupply = await updateSupply(editingSupply.id, supplyData)
        setSupplies(supplies.map(s => 
          s.id === editingSupply.id ? updatedSupply : s
        ))
      } else {
        const newSupply = await createSupply(supplyData)
        setSupplies([...supplies, newSupply])
      }
      setIsDialogOpen(false)
    } catch (error) {
      console.error('Error saving supply:', error)
      // Handle error
    }
  }

  const filteredSupplies = supplies.filter(supply => 
    supply.name.toLowerCase().includes(searchTerm.toLowerCase())
  )

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6 p-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Insumos</h1>
          <p className="text-muted-foreground">Gerencie seus insumos e estoque</p>
        </div>
        <Button onClick={() => handleOpenDialog()}>
          <Plus className="mr-2 h-4 w-4" />
          Adicionar Insumo
        </Button>
      </div>

      <div className="rounded-md border bg-white">
        <div className="p-4 border-b">
          <Input
            placeholder="Buscar insumos..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="max-w-sm"
          />
        </div>
        
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="text-left">Nome</TableHead>
              <TableHead className="text-left">Unidade</TableHead>
              <TableHead className="text-left">Custo Unitário</TableHead>
              <TableHead className="text-left">Estoque Atual</TableHead>
              <TableHead className="text-left">Estoque Mínimo</TableHead>
              <TableHead className="text-left">Categoria</TableHead>
              <TableHead className="w-[120px] text-left">Ações</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filteredSupplies.length === 0 ? (
              <TableRow>
                <TableCell colSpan={6} className="h-24 text-center">
                  Nenhum insumo encontrado
                </TableCell>
              </TableRow>
            ) : (
              filteredSupplies.map((supply) => (
                <TableRow key={supply.id}>
                  <TableCell className="font-medium">{supply.name}</TableCell>
                  <TableCell>
                    {{
                      'g': 'g',
                      'kg': 'kg',
                      'ml': 'ml',
                      'l': 'L',
                      'un': 'un'
                    }[supply.unit]}
                  </TableCell>
                  <TableCell>
                    {new Intl.NumberFormat('pt-BR', {
                      style: 'currency',
                      currency: 'BRL',
                    }).format(supply.cost_per_unit)}
                  </TableCell>
                  <TableCell>{supply.stock_quantity}</TableCell>
                  <TableCell>{supply.min_stock}</TableCell>
                  <TableCell className="text-muted-foreground">
                    {supply.category || '-'}
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <Button 
                        variant="ghost" 
                        size="icon"
                        onClick={() => handleOpenDialog(supply)}
                      >
                        <Pencil className="h-4 w-4" />
                      </Button>
                      <Button 
                        variant="ghost" 
                        size="icon" 
                        onClick={() => handleDelete(supply.id)}
                      >
                        <Trash2 className="h-4 w-4 text-destructive" />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>

      {/* Add/Edit Dialog */}
      {isDialogOpen && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl w-full max-w-md">
            <div className="p-6">
              <h2 className="text-xl font-semibold mb-4">
                {editingSupply ? 'Editar Insumo' : 'Novo Insumo'}
              </h2>
              
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Nome do Insumo
                  </label>
                  <Input
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({...formData, name: e.target.value})}
                    placeholder="Ex: Farinha de trigo"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Categoria (opcional)
                  </label>
                  <Input
                    type="text"
                    value={formData.category}
                    onChange={(e) => setFormData({...formData, category: e.target.value})}
                    placeholder="Ex: Ingredientes"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Unidade
                    </label>
                    <select
                      value={formData.unit}
                      onChange={(e) => setFormData({...formData, unit: e.target.value as Unit})}
                      className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                      required
                    >
                      <option value="un">Unidade (un)</option>
                      <option value="g">Gramas (g)</option>
                      <option value="kg">Quilogramas (kg)</option>
                      <option value="ml">Mililitros (ml)</option>
                      <option value="l">Litros (L)</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Custo Unitário (R$)
                    </label>
                    <Input
                      type="number"
                      step="0.01"
                      min="0"
                      value={formData.cost_per_unit}
                      onChange={(e) => setFormData({...formData, cost_per_unit: e.target.value})}
                      placeholder="Ex: 5.00"
                      required
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Estoque Atual
                    </label>
                    <Input
                      type="number"
                      step="0.1"
                      min="0"
                      value={formData.stock_quantity}
                      onChange={(e) => setFormData({...formData, stock_quantity: e.target.value})}
                      placeholder="Ex: 1.00"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Estoque Mínimo
                    </label>
                    <Input
                      type="number"
                      step="0.1"
                      min="0"
                      value={formData.min_stock}
                      onChange={(e) => setFormData({...formData, min_stock: e.target.value})}
                      placeholder="Ex: 0.50"
                      required
                    />
                  </div>
                </div>

                <div className="flex justify-end space-x-3 pt-4">
                  <Button
                    type="button"
                    variant="outline"
                    onClick={() => setIsDialogOpen(false)}
                  >
                    Cancelar
                  </Button>
                  <Button type="submit">
                    {editingSupply ? 'Salvar' : 'Adicionar'}
                  </Button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}