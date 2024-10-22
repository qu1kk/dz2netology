from functools import lru_cache

@lru_cache()
def min_breaks(n: int, m: int) -> int:
    if n == 1 and m == 1:
        return 0
        
    if n == 1:
        return m -1
        
    if m == 1:
        return n - 1
        
    horizontal_cut = min_breaks(n // 2, 3) + min_breaks( n - n // 2, m) + 1 
    vertical_cut = min_breaks(n, m // 2) + min_breaks(n, m-m//2) + 1 
    
    return min(horizontal_cut,vertical_cut)
    
print(min_breaks(2, 3))
print(min_breaks(3, 3))
print(min_breaks(1, 1))