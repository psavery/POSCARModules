
# Returns the crystal family's pearson symbol
# triclinic:    a
# monoclinic:   m
# orthorhombic: o
# tetragonal:   t
# hexagonal:    h
# cubic:        c
def spgNumToLatticeSymbol(spgNum):
  if spgNum < 1 or spgNum > 230:
    print("Error in spgNumToLatticeSymbol: spgNum", spgNum, \
          "is not a valid space group number")
    return ''

  # Triclinic
  if spgNum < 3:
    return 'a'

  # Monoclinic
  if spgNum < 16:
    return 'm'

  # Orthorhombic
  if spgNum < 75:
    return 'o'

  # Tetragonal
  if spgNum < 143:
    return 't'

  # Hexagonal
  if spgNum < 195:
    return 'h'

  # Cubic
  return 'c'
