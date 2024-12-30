from checkers import checkout, getout
import yaml


with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestPositive:
    def test_step1(self, create_folders, clear_folders, create_files, print_time):
        # Проверка добавления файлов в архив и наличия файла с архивом в папке
        res1 = checkout("cd {}; 7z a {}/arx4 -t{}".format(data["folder_in"], data["folder_out"], data["type"]), "Everything is Ok")
        res2 = checkout("ls {}".format(data["folder_out"]), "arx4.{}".format(data["type"]))
        assert res1 and res2, "test1 - файлы не добавлены в архив или файл с архивом отсутствует в указанной папке"

    def test_step2(self, clear_folders, create_files):
        # Проверка распаковки архива и наличие распакованных файлов в папке
        res = []
        res.append(checkout("cd {}; 7z a {}/arx -t{}".format(data["folder_in"], data["folder_out"], data["type"]), "Everything is Ok"))
        res.append(checkout("cd {}; 7z e arx.{} -o{} -y".format(data["folder_out"], data["type"], data["folder_ext"]), "Everything is Ok"))
        for item in create_files:
            res.append(checkout("ls {}".format(data["folder_ext"]), item))
        assert all(res), "test2 -  ошибка распаковки архива или распакованные файлы отсутствуют в указанной папке"

    def test_step3(self, clear_folders, create_files):
        # Проверка вывода списка файлов (l)
        res = []
        res.append(checkout("cd {}; 7z a {}/arx -t{}".format(data["folder_in"], data["folder_out"], data["type"]), "Everything is Ok"))
        for item in create_files:
            res.append(checkout("cd {}; 7z l arx.{}".format(data["folder_out"], data["type"]), item))
        assert all(res), "test3 - не удалось найти файлы в архиве"

    def test_step4(self, clear_folders, create_files, create_subfolder):
        # Проверка разархивирования с путями (x)
        res = []
        res.append(checkout("cd {}; 7z a {}/arx -t{}".format(data["folder_in"], data["folder_out"], data["type"]), "Everything is Ok"))
        res.append(checkout("cd {}; 7z x arx.{} -o{} -y".format(data["folder_out"], data["type"], data["folder_ext2"]), "Everything is Ok"))
        for item in create_files:
            res.append(checkout("ls {}".format(data["folder_ext2"]), item))
        res.append(checkout("ls {}".format(data["folder_ext2"]), create_subfolder[0]))
        res.append(checkout("ls {}/{}".format(data["folder_ext2"], create_subfolder[0]), create_subfolder[1]))
        assert all(res), "test4 - не удалось разархивировать с сохранением путей"

    def test_step5(self, clear_folders, create_files):
    # Проверка расчета хеша (h)
        res = []
        for item in create_files:
            res.append(checkout("cd {}; 7z h {}".format(data["folder_in"], item), "Everything is Ok"))
            com_7z = "cd {}; 7z h -{} {} | grep CRC32 | awk '{{print $4}}'".format (data["folder_in"],data["alg_hash"], item)
            res_hash = getout("cd {}; crc32 {}".format(data["folder_in"], item)).upper()
            res.append(checkout(com_7z, res_hash))
        assert all(res), "test5 - хеш файла не совпадает с ожидаемым значением"

    def test_step6(self):
        # Проверка удаления
        res = []
        res.append(checkout("cd {}; 7z a {}/arx -t{}".format(data["folder_in"], data["folder_out"], data["type"]),"Everything is Ok"))
        res.append(checkout("cd {}; 7z d arx.{}".format(data["folder_out"], data["type"]), "Everything is Ok"))
        assert all(res), "test6 - не удалось удалить архив"