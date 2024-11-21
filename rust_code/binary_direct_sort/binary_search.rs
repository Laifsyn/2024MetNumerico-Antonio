use std::fmt::Display;
use std::mem;

pub struct BinaryInsertionSort<'a, T> {
    data: &'a mut [T],
    // Equivalente en C: `T* data;`
    // Equivalente en Java: `Object[] data;`
    // Equivalente en Python: `List[Object]`
    sorted_until: usize,
    // Equivalente en C: `size_t sorted_until;`
    // Equivalente en Java: `int sortedUntil;`
    // Equivalente en Python: `int sorted_until`
}

impl<'a, T> BinaryInsertionSort<'a, T>
where
    T: Ord + Display,
{
    pub fn new(data: &'a mut [T]) -> Self {
        BinaryInsertionSort {
            data,
            sorted_until: 1, // Se considera que el elemento `0` está ordenado
        }
    }

    pub fn peek(&self) -> &[T] {
        self.data
    }

    pub fn sorted_until(&self) -> usize {
        self.sorted_until
    }

    /// Búsqueda binaria para encontrar la posición de inserción.
    fn binary_search(&self, compare_value: T) -> usize {
        let (mut left, mut right) = (0, self.sorted_until);
        // C: `size_t left = 0, right = self->sorted_until;`
        // Java: `int left = 0, right = self.sortedUntil;`
        // Python: `left, right = 0, self.sorted_until`

        // Realizar la búsqueda binaria
        while left < right {
            let middle = (left + right) / 2;
            if compare_value < self.data[middle] {
                right = middle;
            } else {
                left = middle + 1;
            }
        }
        // C:
        // while (left < right) {
        //     size_t middle = (left + right) / 2;
        //     if (compare_value < self->data[middle]) {
        //         right = middle;
        //     } else {
        //         left = middle + 1;
        //     }
        // }
        //
        // Python:
        // while left < right:
        //     middle = (left + right) // 2
        //     if compare_value < self.data[middle]:
        //         right = middle
        //     else:
        //         left = middle + 1

        left
    }
}

impl<'a, T> Iterator for BinaryInsertionSort<'a, T>
where
    T: Ord + Display + Clone,
{
    type Item = ();

    fn next(&mut self) -> Option<Self::Item> {
        if self.sorted_until >= self.data.len() {
            return None;
        }

        let indice_inserción = self.binary_search(self.data[self.sorted_until].clone());
        // Mover los elementos a la derecha para hacer espacio para el valor
        // a insertar en el índice se inserción
        for i in (indice_inserción..self.sorted_until).rev() {
            let (left, right) = self.data.split_at_mut(i + 1);
            mem::swap(&mut left[i], &mut right[0]);
        }
        // C:
        // for (size_t i = self->sorted_until; i > insert_position; i--) {
        //     self->data[i] = self->data[i - 1];
        // }
        // Python:
        // for i in range(self.sorted_until, insert_position, -1):
        //     self.data[i], self.data[i - 1] = self.data[i - 1], self.data[i]

        // Actualizar el puntero hacia el siguiente elemento sin ordenar
        self.sorted_until += 1;
        Some(())
    }
}

pub fn main() {
    let mut data = vec![5, 2, 7, 9, 1, 6];
    data.sort();
    data = data.into_iter().rev().collect();
    println!("Data: {:?}", data);
    let mut sorter = BinaryInsertionSort::new(&mut data);

    // Step-by-step iteration

    while let Some(_) = sorter.next() {
        println!("Sorted data:  {:?}", sorter.peek());
    }
}
