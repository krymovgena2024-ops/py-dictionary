from dataclasses import dataclass
from typing import Any
from collections.abc import Hashable


@dataclass
class Node:
    key: Any
    value: Any
    hash_node: int


class Dictionary:
    def __init__(self) -> None:
        self.length = 0
        self.hash_table = [None for _ in range(8)]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        capacity = len(self.hash_table)
        if len(self) >= int(capacity * (2 / 3)):
            new_hash_table = [None for _ in range(capacity * 2)]
            new_capacity = len(new_hash_table)
            self.length = 0
            self.resize_hash_table(key, value, new_capacity, new_hash_table)
            hash_new_key = hash(key)
            index_new_item = hash_new_key % new_capacity
            new_node = Node(key, value, hash_new_key)
            self.save_item_in_table_if_resize_happened(
                new_hash_table,
                new_capacity,
                index_new_item,
                new_node,
                key,
                value)
            self.hash_table = new_hash_table
            return
        hash_key = hash(key)
        node = Node(key, value, hash_key)
        initial_index = hash_key % capacity
        self.save_item_in_table(node, initial_index, key, value)

    def save_item_in_table(
            self,
            node: Node,
            initial_index: int,
            key: Any,
            value: Any) -> None:
        capacity = len(self.hash_table)
        if self.hash_table[initial_index] is None:
            self.hash_table[initial_index] = node
            self.length += 1
            return
        if self.hash_table[initial_index].key == key:
            self.hash_table[initial_index].value = value
            return
        if self.hash_table[initial_index].key != key:
            perturb = hash(key)
            last_index = initial_index
            while True:
                current_index = (5 * last_index + 1 + perturb) % capacity
                last_index = current_index
                perturb = perturb >> 5
                if self.hash_table[current_index] is None:
                    self.hash_table[current_index] = node
                    self.length += 1
                    return
                if self.hash_table[current_index].key == key:
                    self.hash_table[current_index].value = value
                    return

    def resize_hash_table(
            self,
            key: Hashable,
            value: Any,
            new_capacity: int,
            new_hash_table: list) -> None:
        for item in self.hash_table:
            if isinstance(item, Node):
                initial_index = item.hash_node % new_capacity
                if new_hash_table[initial_index] is None:
                    new_hash_table[initial_index] = item
                    self.length += 1
                    continue
                if new_hash_table[initial_index].key == item.key:
                    new_hash_table[initial_index].value = value
                    continue
                if new_hash_table[initial_index].key != item.key:
                    last_index = initial_index
                    item_hash = item.hash_node
                    while True:
                        example = (5 * last_index + 1 + item_hash)
                        curent_index = example % new_capacity
                        last_index = curent_index
                        item_hash = item_hash >> 5
                        if new_hash_table[curent_index] is None:
                            new_hash_table[curent_index] = item
                            self.length += 1
                            break
                        if new_hash_table[curent_index].key == key:
                            new_hash_table[curent_index].value = item.value
                            break

    def save_item_in_table_if_resize_happened(
            self,
            new_hash_table: list,
            new_capacity: int,
            index_new_item: int,
            new_node: Node,
            key: Hashable,
            value: Any) -> None:
        if new_hash_table[index_new_item] is None:
            new_hash_table[index_new_item] = new_node
            self.length += 1
            self.hash_table = new_hash_table
            return
        if new_hash_table[index_new_item].key == key:
            new_hash_table[index_new_item].value = value
            self.hash_table = new_hash_table
            return
        if new_hash_table[index_new_item].key != key:
            perturb = hash(key)
            last_index = index_new_item
            while True:
                base_index = (5 * last_index + 1 + perturb)
                current_index = base_index % new_capacity
                last_index = current_index
                perturb = perturb >> 5
                if new_hash_table[current_index] is None:
                    new_hash_table[current_index] = new_node
                    self.length += 1
                    break
                if new_hash_table[current_index].key == key:
                    new_hash_table[current_index].value = value
                    break

    def find_index_and_get_item(
            self,
            key: Hashable,
            capacity: int,
            hash_key: int) -> Any:
        initial_index = hash_key % capacity
        item = self.hash_table[initial_index]
        if item is None:
            raise KeyError(f"Key '{key}' not found")
        if item.key == key:
            return item.value
        if item.key != key:
            perturb = hash(key)
            last_index = initial_index
            while True:
                current_index = (5 * last_index + 1 + perturb) % capacity
                last_index = current_index
                perturb = perturb >> 5
                if self.hash_table[current_index] is None:
                    raise KeyError(f"Key '{key}' not found")
                if self.hash_table[current_index].key == key:
                    return self.hash_table[current_index].value

    def __getitem__(self, key: Hashable) -> Any:
        capacity = len(self.hash_table)
        hash_key = hash(key)
        return self.find_index_and_get_item(
            key,
            capacity,
            hash_key)

    def __len__(self) -> Any:
        return self.length
