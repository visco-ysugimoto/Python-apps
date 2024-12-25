import flet as ft
import os

class SaveModeManager:
    def __init__(self):
        self.save_mode = "0"  # デフォルト値

    def set_save_mode(self, mode):
        self.save_mode = mode

    def get_save_mode(self):
        return self.save_mode

class CameraSelectionManager:
    def __init__(self):
        self.selected_cameras = []

    def select_camera(self, camera_id):
        if camera_id not in self.selected_cameras:
            self.selected_cameras.append(camera_id)

    def deselect_camera(self, camera_id):
        if camera_id in self.selected_cameras:
            self.selected_cameras.remove(camera_id)

    def get_selected_cameras(self):
        return self.selected_cameras

class ImageProcessor:
    def __init__(self, log_file_path):
        self.log_file_path = log_file_path

    def parse_log(self):
        # ログファイル解析処理
        cam_info_dict = {}
        try:
            with open(self.log_file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    # パターンマッチング処理
                    pass
        except FileNotFoundError:
            print(f"Log file {self.log_file_path} not found.")
        return cam_info_dict

    def process_images(self, folder_path, selected_cameras, save_mode):
        # 画像処理ロジック
        if not os.path.exists(folder_path):
            print(f"Folder {folder_path} does not exist.")
            return

        for file_name in os.listdir(folder_path):
            if file_name.endswith(".bmp"):
                if self.should_save(file_name, selected_cameras, save_mode):
                    print(f"Processing file: {file_name}")

    def should_save(self, file_name, selected_cameras, save_mode):
        # 保存条件を判定
        return True

def main(page: ft.Page):
    page.title = "タスク画像保存フロー"
    page.vertical_alignment = ft.MainAxisAlignment.START

    # モジュールのインスタンス化
    save_mode_manager = SaveModeManager()
    camera_selection_manager = CameraSelectionManager()
    image_processor = ImageProcessor(log_file_path="path/to/log")
  
    # カメラ選択のUI
    def on_camera_toggle(e, cam_id):
        if e.control.value:
            camera_selection_manager.select_camera(cam_id)
        else:
            camera_selection_manager.deselect_camera(cam_id)

    camera_checkboxes_container = ft.Column()

    camera_checkboxes = [
        ft.Checkbox(label=f"Camera {i}", value=False, on_change=lambda e, cam_id=i: on_camera_toggle(e, cam_id))
        for i in range(1, 5)
    ]

    camera_checkboxes_container.controls.extend(camera_checkboxes)
    page.add(ft.Text("カメラを選択:"), camera_checkboxes_container)

    def toggle_label(e):
        switch.label = "全て保存" if switch.value else "部分保存"
        camera_checkboxes_container.visible = switch.value
        camera_checkboxes_container.update()
        switch.update()

    switch = ft.CupertinoSwitch(value=True, label="全て保存", on_change=toggle_label)
    page.add(switch)

    # フォルダ選択ダイアログ
    folder_path_label = ft.Text("選択したフォルダ: 未選択")
    folder_path = [None]  # 使用するためにリストでラップ

    def select_folder(e):
        def on_result(result):
            try:
                if result.files:
                    folder_path[0] = result.files[0].path
                    folder_path_label.value = f"選択したフォルダ: {folder_path[0]}"
                else:
                    folder_path_label.value = "フォルダが選択されていません。"
            except Exception as ex:
                folder_path_label.value = f"エラーが発生しました: {ex}"
            folder_path_label.update()

        try:
            file_picker = ft.FilePicker(on_result=on_result, allow_directories=True)
            page.overlay.append(file_picker)
            file_picker.pick()
        except Exception as ex:
            folder_path_label.value = f"フォルダ選択の初期化エラー: {ex}"
            folder_path_label.update()

    page.add(ft.ElevatedButton("フォルダ選択", on_click=select_folder), folder_path_label)
  
    # 保存モード選択
    save_mode_text = ft.Text("保存モードを選択:")
    save_mode_options = ft.RadioGroup(
        value="0",
        on_change=lambda e: save_mode_manager.set_save_mode(e.control.value),
        content=ft.Column([
            ft.Radio(value="0", label="全保存"),
            ft.Radio(value="1", label="コメント付き保存"),
            ft.Radio(value="2", label="ロック画像保存"),
        ])
    )
    save_mode_options.visible = switch.value
    save_mode_text.visible = switch.value
    page.add(save_mode_text, save_mode_options)
    
    # 圧縮率スライダー
    slider = ft.Slider(
        min=10,
        max=100,
        divisions=9,
        label="{value}%",
        value=100,
    )
    page.add(ft.Text("圧縮率を選択:"), slider)

    # 画像処理の実行ボタン
    def execute_processing(e):
        if not folder_path[0]:
            page.snack_bar = ft.SnackBar(content=ft.Text("フォルダを選択してください。"))
            page.snack_bar.open()
            return

        selected_cameras = camera_selection_manager.get_selected_cameras()
        save_mode = save_mode_manager.get_save_mode()
        image_processor.process_images(folder_path=folder_path[0], selected_cameras=selected_cameras, save_mode=save_mode)
        page.add(ft.Text("画像処理が完了しました！"))

    page.add(ft.ElevatedButton("画像処理を実行", on_click=execute_processing))

ft.app(target=main)
