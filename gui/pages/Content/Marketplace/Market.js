import React, {useState, useEffect} from 'react';
import Image from "next/image";
import styles from './Market.module.css';
import MarketKnowledge from './MarketKnowledge';
import MarketAgent from './MarketAgent';
import MarketTools from './MarketTools';
import ToolkitTemplate from './ToolkitTemplate';
import {EventBus} from "@/utils/eventBus";
import AgentTemplate from "./AgentTemplate";
import KnowledgeTemplate from "./KnowledgeTemplate";
import {setLocalStorageValue, setLocalStorageArray} from "@/utils/utils";

export default function Market({env}) {
  const [activeTab, setActiveTab] = useState('market_tools');
  const [itemClicked, setItemClicked] = useState(false);
  const [templateData, setTemplateData] = useState([]);
  const [detailType, setDetailType] = useState('');

  useEffect(() => {
    const marketplace_tab = localStorage.getItem('marketplace_tab');
    if (marketplace_tab) {
      setActiveTab(marketplace_tab);
    }

    const item_clicked = localStorage.getItem('market_item_clicked');
    const detail_type = localStorage.getItem('market_detail_type');
    const market_item = localStorage.getItem('market_item');

    if (item_clicked) {
      setItemClicked(JSON.parse(item_clicked));
      if (detail_type) {
        setDetailType(item_clicked === 'true' ? detail_type : '');
        setTemplateData(item_clicked === 'true' ? JSON.parse(market_item) : []);
      }
    }

    const handleOpenTemplateDetails = ({item, contentType}) => {
      setLocalStorageValue('market_detail_type', contentType, setDetailType);
      setLocalStorageArray('market_item', item, setTemplateData);
      setLocalStorageValue('market_item_clicked', true, setItemClicked);
    };

    const handleBackClick = () => {
      setLocalStorageValue('market_item_clicked', false, setItemClicked);
    }

    EventBus.on('openTemplateDetails', handleOpenTemplateDetails);
    EventBus.on('goToMarketplace', handleBackClick);

    return () => {
      EventBus.off('openTemplateDetails', handleOpenTemplateDetails);
      EventBus.off('goToMarketplace', handleBackClick);
    };
  }, []);

  const switchTab = (tab) => {
    setActiveTab(tab);
    localStorage.setItem('marketplace_tab', tab);
  };

  return (
    <div>
      {!itemClicked ? <div className={styles.empty_state}>
        <div style={{width: '100%', display: 'flex', flexDirection: 'column'}}>
          <div className={styles.detail_top}>
            <div style={{display: 'flex', overflowX: 'scroll', marginLeft: '8px'}}>
              <button onClick={() => switchTab('market_tools')} className={activeTab === 'market_tools' ? 'tab_button_selected' : 'tab_button'}>
                <Image width={14} height={14} src="/images/tools_light.svg" alt="tools-icon"/>
                <span>Tools</span>
              </button>
              <button onClick={() => switchTab('market_knowledge')} className={activeTab === 'market_knowledge' ? 'tab_button_selected' : 'tab_button'}>
                <Image width={14} height={14} src="/images/knowledge.svg" alt="knowledge-icon"/>
                <span>Knowledge</span>
              </button>
              <button onClick={() => switchTab('market_agents')} className={activeTab === 'market_agents' ? 'tab_button_selected' : 'tab_button'}>
                <Image width={14} height={14} src="/images/agents_light.svg" alt="agent-template-icon"/>
                <span>Agent Templates</span>
              </button>
              <button onClick={() => switchTab('market_models')} className={activeTab === 'market_models' ? 'tab_button_selected' : 'tab_button'}>
                <Image width={14} height={14} src="/images/models.svg" alt="model-template-icon"/>
                <span>Models</span>
              </button>
            </div>
          </div>
          <div>
            {activeTab === 'market_tools' && <MarketTools/>}
            {activeTab === 'market_knowledge' && <MarketKnowledge/>}
            {activeTab === 'market_agents' && <MarketAgent/>}
          </div>
        </div>
      </div> : <div style={{padding: '0 3px'}}>
        {detailType === 'agent_template' && <AgentTemplate env={env} template={templateData}/>}
        {detailType === 'knowledge_template' && <KnowledgeTemplate env={env} template={templateData}/>}
        {detailType === 'tool_template' && <ToolkitTemplate env={env} template={templateData}/>}
      </div>}
    </div>
  );
};

