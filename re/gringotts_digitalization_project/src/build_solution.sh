nasm -felf64 solution.s -o solution.o && ld solution.o -o solution && strip solution && base64 solution
