'''
Created on 13 Feb 2015

@author: Jon

From Numba Array Reductions notebook
'''
import numba as nb
import numpy as np

@nb.autojit
def take( x, idx ):
    r = np.ndarray( idx.shape[0], dtype=x.dtype )
    for i in range( idx.shape[0] ):
        r[i]=x[ idx[ i ] ]
    return r

@nb.autojit
def take_to_out( x, idx, r ):    
    for i in range( idx.shape[0] ):
        r[i]=x[ idx[ i ] ]

@nb.autojit
def square_take( source, idx ):
    """ Take from source, a 2d array """
    r = np.empty( ( idx.shape[0], idx.shape[0] ) )
    square_take_to_out( source, idx, r )
    return r

@nb.autojit( nopython=True )
def square_take_to_out( source, idx, out ):
    """ Take from source, a 2d array, with results going to out """
    for i in range( idx.shape[0] ):
        for j in range( idx.shape[0] ):
            out[ i, j ] = source[ idx[i], idx[j] ]
            
@nb.autojit( nopython=True )
def square_and_rect_take_to_out( source, idx0, idx1, out ):
    """ Take from source, a 2d array, with results going to out
        On the left is the square array from idx
        On the right is the rect array with rows from idx0, cols from idx1
        This is useful for optimising portfolios
    """
    for i in range( idx0.shape[0] ):
        for j in range( idx0.shape[0] ):
            out[ i, j ] = source[ idx0[i], idx0[j] ]
        k = idx0.shape[0]
        for j in range( idx1.shape[0] ):
            out[ i, k ] = source[ idx0[i], idx1[j ]]
            k+=1
            
@nb.autojit
def swap_row_cols( X, i, j ):
    """ Swap the rows and cols of X indexed by i and j """

    for a in range( X.shape[0] ):
        t = X[ a, j ]
        X[ a, j ] = X[ a, i ]
        X[ a, i ] = t
        
    for a in range( X.shape[0] ):
        t = X[ j, a ]
        X[ j, a ] = X[ i, a ]
        X[ i, a ] = t
            