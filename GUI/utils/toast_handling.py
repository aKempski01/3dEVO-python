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

def error_select_all_toast(relative_widget):
    toast = Toast(relative_widget)
    toast.setDuration(10000)
    toast.setTitle('Error!!!')
    toast.setText('All plots were not selected due to the contradictory experiments in runs folder. Please select manually one experiment and press the the SELECT ALL button once again.')
    toast.applyPreset(ToastPreset.ERROR)  # Apply style preset
    toast.setAlwaysOnMainScreen(True)
    Toast.setPositionRelativeToWidget(relative_widget)
    toast.show()

