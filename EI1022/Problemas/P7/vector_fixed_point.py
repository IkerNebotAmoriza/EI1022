def busca_punto_fijo_recursiva(v):
    def rec(begin:int, end:int):
        if end - begin == 0:
            return None
        half = (begin + end) // 2
        if v[half] < half:
            return rec(half, end)
        if v[half] > half:
            return rec(begin, half)
        else:
            return half
    return rec(0, len(v))


def busca_punto_fijo_iterativa(v):
    # IMPLEMENTAR TODO
    pass


def busca_punto_pico(v):
    def rec(begin:int, end:int):
        if end-begin == 1: return begin
        half = (begin + end)// 2
        if v[half-1] <= v[half]:
            return rec(half, end)
        return rec(begin, half)
    return rec(0, len(v))

def busca_subvector_maximo(v):
    def rec(b:int, e:int):
        if  e-b == 1: return v[b]
        h=(b+e)//2
        m_izq = rec(b, h)
        m_der = rec(h, e)
        # IMPLEMENTAR LA ASIGNACION
        m_mitad =
        return max(m_izq, m_der, m_mitad)
    return rec(0, len(v))