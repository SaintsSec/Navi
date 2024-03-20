#include <libxfce4panel/xfce-panel-plugin.h>
#include <exo/exo.h>

static void python_script_launcher(XfcePanelPlugin *plugin)
{
    const gchar* terminal_emulator = exo_execute_preferred_application("TerminalEmulator", NULL, NULL, NULL, NULL);
    system(terminal_emulator + " -e 'python3 /opt/Navi/navi-shell.py'");
}

static void construct(XfcePanelPlugin *plugin)
{
    gtk_widget_show_all(gtk_button_new_with_label("Navi"));

    g_signal_connect(plugin, "clicked", G_CALLBACK(python_script_launcher), NULL);
}

XFCE_PANEL_PLUGIN_REGISTER(construct);
