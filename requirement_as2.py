

def plot_general(features_1,features_2,features_3):
    #ploting frequency
    time_1 = np.linspace(0,features_1.shape[1]*0.015,features_1.shape[1])
    time_2 = np.linspace(0,features_2.shape[1]*0.015,features_2.shape[1])
    time_3 = np.linspace(0,features_3.shape[1]*0.015,features_3.shape[1])
    fig, (ax1, ax2,ax3) = plt.subplots(3)
    ax1.semilogy(time_1,features_1[0,:])
    ax2.semilogy(time_2,features_2[0,:])
    ax3.semilogy(time_3,features_3[0,:])
    ax1.set(ylim=[100,300],xlim=[0,7.5],xlabel="time (s)",ylabel="frequency (Hz)", title="Melody 1")
    ax2.set(ylim=[100,300],xlim=[0,7.5],xlabel="time (s)",ylabel="frequency (Hz)", title="Melody 2")
    ax3.set(ylim=[100,300],xlim=[0,7.5],xlabel="time (s)",ylabel="frequency (Hz)", title="Melody 3")
    fig.suptitle("Pitch profiles")

    #ploting intensity
    fig, (ax1, ax2,ax3) = plt.subplots(3)
    ax1.plot(time_1,features_1[2,:])
    ax2.plot(time_2,features_2[2,:])
    ax3.plot(time_3,features_3[2,:])
    ax1.set(xlim=[0,7.5],xlabel="time (s)",ylabel="Intensity", title="Melody 1")
    ax2.set(xlim=[0,7.5],xlabel="time (s)",ylabel="Intensity", title="Melody 2")
    ax3.set(xlim=[0,7.5],xlabel="time (s)",ylabel="Intensity", title="Melody 3")
    fig.suptitle("Intensity profiles")

def plot_melody(features,title="Melody"):
    time = np.linspace(0,features.shape[1]*0.015,features.shape[1])
    fig, (ax1, ax2,ax3) = plt.subplots(3)
    ax1.semilogy(time,features[0,:])
    ax2.plot(time,features[1,:])
    ax3.plot(time,features[2,:])
    ax1.set(ylim=[100,300],xlabel="time (s)",ylabel="frequency (Hz)", title="Frequency")
    ax2.set(xlabel="time (s)",ylabel="rho", title="Correlation")
    ax3.set(xlabel="time (s)",ylabel="Intensity", title="Intensity")
    fig.suptitle(title)

def plot_ex_features(ex_feature_1,ex_feature_2,ex_feature_3):
    time_1 = np.linspace(0,ex_feature_1.size*0.015,ex_feature_1.size)
    time_2 = np.linspace(0,ex_feature_2.size*0.015,ex_feature_2.size)
    time_3 = np.linspace(0,ex_feature_3.size*0.015,ex_feature_3.size)
    fig, (ax1, ax2,ax3) = plt.subplots(3)
    ax1.plot(time_1,ex_feature_1)
    ax2.plot(time_2,ex_feature_2)
    ax3.plot(time_3,ex_feature_3)
    ax1.set(xlabel="time (s)",ylabel="feature", title="Melody 1")
    ax2.set(xlabel="time (s)",ylabel="feature", title="Melody 2")
    ax3.set(xlabel="time (s)",ylabel="feature", title="Melody 3")
    fig.suptitle("Feature profile")


if __name__ == "__main__":
    from __init__ import *
    
    #extracting melody_1
    fs_1, signal_1 = wavfile.read("Songs/melody_1.wav")
    features_1 = GetMusicFeatures(signal_1,fs_1)
    
    #extracting melody_2
    fs_2, signal_2 = wavfile.read("Songs/melody_2.wav")
    features_2 = GetMusicFeatures(signal_2,fs_2)
    
    #extracting melody_3
    fs_3, signal_3 = wavfile.read("Songs/melody_3.wav")
    features_3 = GetMusicFeatures(signal_3,fs_3)
    
    # plot_melody(features_1,"melody 1")
    # plot_melody(features_2,"melody 2")
    
    #first requirement :
    #plot pitch and intensity of the three recordings
    plot_general(features_1, features_2, features_3)
    
    #third requirement :
    #feature extractor
    ex_feature_1 = main_extractor(features_1)
    ex_feature_2 = main_extractor(features_2)
    ex_feature_3 = main_extractor(features_3)
    
    #fourth requirement :
    #plot extracted features
    plot_ex_features(ex_feature_1, ex_feature_2, ex_feature_3)
    
    #fifth requirement :
    #Plot original vs transposed
    plt.figure()
    ex_transposed_feature_1 = main_extractor(features_1*1.5)
    time = np.linspace(0,ex_feature_1.size*0.015,ex_feature_1.size)
    plt.plot(time,ex_feature_1)
    plt.plot(time,ex_transposed_feature_1)
    plt.xlabel("time (s)")
    plt.suptitle("Feature from original vs. feature from transposed")
    plt.legend(["original","transposed"])
    
    
    plt.show()
