from pyqttoast import Toast, ToastPreset


def show_save_plot_toast(relative_widget, save_path: str):
    toast = Toast(relative_widget)
    toast.setDuration(10000)
    toast.setTitle('Success! The plot was saved.')
    toast.setText('save path: ' + save_path)
    toast.applyPreset(ToastPreset.SUCCESS)  # Apply style preset
    toast.setAlwaysOnMainScreen(True)
    Toast.setPositionRelativeToWidget(relative_widget)
    toast.show()

