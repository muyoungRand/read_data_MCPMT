#%%
import json

def get_set(filename):
    with open(filename) as f:
        file = json.loads(f.read())

    # AWG settings is obtained from sequence file, so ignored here EXCEPT the scan parameters

    # Look at DDS settings, and extract relevant data
    # E.g) If SingleTone mode -> Only get FreqWord and AmplitudeWord values
    # E.g) If 4-tone mode -> Figure out levels -> Get all frequencies and amplitudes
    dds = file['dds']['ddslist']

    dds_names = list(dds.keys())

    # List of properties to extract for a given DDS mode
    # Update this list for other DDS modes, only singletone and FM are implemented here
    singletone_properties = ['freq0', 'ampl0', 'freq1', 'ampl1']
    others_properties = ['freq0', 'freq1ch0', 'freq2ch0', 'freq3ch0', 'freq1', 'freq1ch1', 'freq2ch1', 'freq3ch1']

    dds_properties = []
    for name in dds_names:
        dev = dds[name] # To simplify notation
        
        mode = dev['mode'] # DDS Mode
        
        dev_dict = {} # To extract relevant data
        dev_dict['name'] = name
        dev_dict['mode'] = mode
        
        if mode == 'singletone':
            for prop in singletone_properties:
                dev_dict[prop] = dev[prop]
        else:
            for prop in others_properties:
                dev_dict[prop] = dev[prop]
                
        dds_properties.append(dev_dict)
        
    # Identify which devices have their properties being scanned
    # To simplify notation
    _scanned_ = file['freq_scan']
    scanned = {}
        
    # Returns INDEX 
    dev_index = _scanned_['deviceidx']
    prop_index = _scanned_['propertyidx'] 

    # Get NUMBERS
    dev = _scanned_['devices'][dev_index]['name'] # Name of scanned device
    _numbers_ = list(_scanned_['devices'][dev_index]['properties'].values())[prop_index] # Dictionary containing properties of the scanned device

    scanned['dev'] = dev
    scanned['prop'] = _numbers_['name']
    scanned['start'] = _scanned_['start']
    scanned['stop'] = _scanned_['stop']
    scanned['step'] = _scanned_['step']

    # Repeat in case there's a second scanned parameter
    dev_index2 = _scanned_['deviceidx2']
    prop_index2 = _scanned_['propertyidx2'] 

    dev2 = _scanned_['devices'][dev_index2]['name'] 
    _numbers2_ = list(_scanned_['devices'][dev_index2]['properties'].values())[prop_index2]

    scanned['dev2'] = dev2
    scanned['prop2'] = _numbers2_['name']
    scanned['start2'] = _scanned_['start2']
    scanned['stop2'] = _scanned_['stop2']
    scanned['step2'] = _scanned_['step2']
    
    return dds_properties, scanned

if __name__=="__main__":
    main()

# %%
